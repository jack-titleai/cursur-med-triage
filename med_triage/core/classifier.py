import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import Dict, Tuple
import re

load_dotenv()

class MessageClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"
        
        # Load the classification prompt template
        self.prompt_template = """
        You are a healthcare message triage system. Analyze the following message and classify it into one of these categories:
        - CRITICAL (Red): Requires immediate attention (< 1 hour)
        - HIGH (Orange): Requires attention within 24 hours
        - MEDIUM (Yellow): Requires attention within 2-3 days
        - LOW (Green): Can be handled when convenient
        - REFERENCE (Blue): Informational, no action needed

        Message Subject: {subject}
        Message Content: {content}

        Provide your classification in the following JSON format:
        {{
            "category": "CATEGORY",
            "confidence": 0.0-1.0,
            "explanation": "Brief explanation of the classification"
        }}
        """

    def classify_message(self, subject: str, content: str) -> Tuple[str, float, str]:
        """
        Classify a message using the LLM.
        
        Args:
            subject: Message subject
            content: Message content
            
        Returns:
            Tuple of (category, confidence_score, explanation)
        """
        prompt = self.prompt_template.format(subject=subject, content=content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a healthcare message triage system."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Get the response content and clean it
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code block markers if present
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'\s*```', '', response_text)
            
            # Try to parse the JSON response
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {response_text}")
                # Fallback to a default classification
                return "MEDIUM", 0.5, "Error parsing classification response"
            
            # Validate the response format
            if not all(key in result for key in ["category", "confidence", "explanation"]):
                print(f"Invalid response format: {result}")
                return "MEDIUM", 0.5, "Invalid classification response format"
            
            # Validate the category
            valid_categories = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "REFERENCE"]
            if result["category"] not in valid_categories:
                print(f"Invalid category: {result['category']}")
                return "MEDIUM", 0.5, "Invalid classification category"
            
            # Validate confidence score
            try:
                confidence = float(result["confidence"])
                if not 0 <= confidence <= 1:
                    confidence = 0.5
            except (ValueError, TypeError):
                confidence = 0.5
            
            return result["category"], confidence, result["explanation"]
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return "MEDIUM", 0.5, f"Error in classification: {str(e)}" 