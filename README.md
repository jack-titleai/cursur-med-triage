# Healthcare Inbox Triage Application

A modern, AI-powered inbox triage system designed specifically for healthcare providers. This application helps healthcare professionals efficiently manage and prioritize their inbox messages using advanced language models.

## Features

- **Intelligent Message Classification**: Uses GPT-4 to automatically classify messages into priority categories
- **Interactive Dashboard**: Beautiful and intuitive web interface for message management
- **Real-time Statistics**: Visual analytics of message distribution and trends
- **Flexible Filtering**: Filter messages by date range and priority category
- **Message Management**: Mark messages as read, reclassify, and add notes
- **Secure & Private**: All processing happens locally with your data

## LLM Integration

This application uses OpenAI's GPT-4 Turbo model for message classification. To use this feature, you'll need:

1. An OpenAI API key (you can get one at https://platform.openai.com/api-keys)
2. A paid OpenAI account with access to GPT-4

### Setting Up API Credentials

1. Create a `.env` file in the project root directory:
```bash
touch .env
```

2. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

⚠️ **Important Security Notes**:
- Never commit your `.env` file to version control
- Keep your API key secure and don't share it with others
- The `.env` file is already included in `.gitignore` to prevent accidental commits

### API Usage and Costs

- The application uses GPT-4 Turbo for message classification
- Each message classification costs approximately $0.01-0.03 (as of 2024)
- The model is configured to be conservative in token usage
- You can monitor your API usage in the OpenAI dashboard

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/med-triage.git
cd med-triage
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Set up your API credentials as described in the LLM Integration section above.

## Usage

### 1. Initialize the Database

```bash
med-triage init-db
```

### 2. Process Messages

To process messages from your CSV file:

```bash
med-triage process-messages inbox_messages.csv
```

The CSV file should have the following columns:
- message_id
- subject
- message
- datetime

### 3. Start the Application

You'll need to run both the API server and the dashboard. Open two terminal windows:

Terminal 1 (API Server):
```bash
med-triage run-api
```

Terminal 2 (Dashboard):
```bash
med-triage run-dashboard
```

The application will be available at:
- API Documentation: http://localhost:8000/docs
- Dashboard: http://localhost:8050

## Triage Categories

The system classifies messages into five categories:

1. **Critical (Red)**
   - Requires immediate attention (< 1 hour)
   - Emergency situations, patient safety concerns

2. **High Priority (Orange)**
   - Requires attention within 24 hours
   - Important lab results, urgent patient questions

3. **Medium Priority (Yellow)**
   - Requires attention within 2-3 days
   - Routine lab results, non-urgent questions

4. **Low Priority (Green)**
   - Can be handled when convenient
   - General information, administrative tasks

5. **Reference (Blue)**
   - Informational, no action needed
   - System updates, general announcements

## Development

### Project Structure

```
med-triage/
├── med_triage/
│   ├── api/            # FastAPI backend
│   ├── core/           # Core functionality
│   ├── dashboard/      # Dash frontend
│   ├── db/            # Database models and connection
│   ├── models/        # Data models
│   └── utils/         # Utility functions
├── tests/             # Test files
├── pyproject.toml     # Project configuration
└── README.md         # This file
```

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- FastAPI for the backend framework
- Dash for the frontend framework
- All contributors and users of this project 