# Healthcare Inbox Triage Classification Scheme

## Overview
This document outlines the classification scheme for healthcare inbox messages. The system is designed to help healthcare providers efficiently prioritize and manage their inbox messages based on urgency, complexity, and required actions.

## Triage Categories

### 1. Critical (Red)
- **Definition**: Messages requiring immediate attention (within 1 hour)
- **Characteristics**:
  - Emergency situations
  - Patient safety concerns
  - Critical lab results
  - Urgent referrals
  - System alerts requiring immediate action
- **Priority Level**: Highest
- **Response Time**: < 1 hour

### 2. High Priority (Orange)
- **Definition**: Messages requiring attention within the same day
- **Characteristics**:
  - Important lab results
  - Urgent patient questions
  - Time-sensitive referrals
  - Medication-related issues
  - Follow-up requests for critical cases
- **Priority Level**: High
- **Response Time**: < 24 hours

### 3. Medium Priority (Yellow)
- **Definition**: Messages requiring attention within 2-3 days
- **Characteristics**:
  - Routine lab results
  - Non-urgent patient questions
  - Regular follow-ups
  - Administrative requests
  - General inquiries
- **Priority Level**: Medium
- **Response Time**: 2-3 days

### 4. Low Priority (Green)
- **Definition**: Messages that can be handled when convenient
- **Characteristics**:
  - General information
  - Non-urgent administrative tasks
  - Marketing materials
  - System notifications
  - General updates
- **Priority Level**: Low
- **Response Time**: Flexible

### 5. Reference (Blue)
- **Definition**: Informational messages requiring no action
- **Characteristics**:
  - Read-only notifications
  - System updates
  - General announcements
  - Archived information
- **Priority Level**: None
- **Response Time**: None

## Classification Criteria
The LLM will classify messages based on:
1. Keywords and phrases indicating urgency
2. Time-sensitive elements
3. Patient safety implications
4. Required actions
5. Message context and complexity
6. Sender information and role

## Implementation Notes
- The LLM will analyze both subject lines and message content
- Classification confidence scores will be provided
- Messages can be reclassified by healthcare providers
- The system will learn from manual reclassifications
- Regular audits will ensure classification accuracy 