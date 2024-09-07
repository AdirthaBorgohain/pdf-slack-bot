# pdf-slack-bot

This project is a PDF processing and question-answering bot that can interact with Slack. It processes PDF documents,
answers questions based on their content, and optionally posts results to Slack.

## Features

- Process PDF documents
- Answer questions based on document content
- Interact with Slack to post results
- Configurable LLM model selection
- Action selection based on user queries
- Streamlit GUI for easy interaction

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AdirthaBorgohain/pdf-slack-bot.git
   cd pdf-slack-bot
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
    - Copy the `.env.example` file to `.env`
    - Fill in the required environment variables in the `.env` file

## Configuration

The project uses environment variables for configuration. Make sure to set the following variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `SLACK_BOT_TOKEN`: Your Slack bot token
- `SLACK_CHANNEL_ID`: The ID of the Slack channel to post messages
- `OPENAI_MODEL`: (Optional) The OpenAI model to use (defaults to a value in `configs.py`)

Refer to the `.env.example` file for a complete list of required environment variables.

## Usage

### Command Line Interface

To run the main script:

```
python main.py
```

This will process the default PDF file (`handbook.pdf`) and answer a set of predefined questions.

### Streamlit GUI

To run the Streamlit GUI:

```
streamlit run gui.py
```

This will start a local web server and open the GUI in your default web browser. With the GUI, you can:

1. Upload a PDF file
2. Enter questions (one per line)
3. Provide an agent query
4. Process the PDF and get answers to your questions
5. Optionally post results to Slack (if the user wants the agent to do so)

### Using Custom PDF Files

You can use any PDF file with this bot. To do so programmatically:

1. Place your PDF file in the `pdf` directory.
2. Update the `PDF_FILENAME` variable in the `main.py` file to match your PDF filename.

For example, if you've added a file named `company_report.pdf` to the `pdf` directory, you would
modify `main.py` as follows:

```python
if __name__ == "__main__":
    import asyncio

    PDF_FILENAME = "company_report.pdf"  # Update this line
    QUESTIONS = [
        # Your questions here
    ]
    AGENT_QUERY = "Answer the questions and post results on Slack"
    asyncio.run(main(PDF_FILENAME, QUESTIONS, AGENT_QUERY))
```

To use the bot programmatically:

```python
import asyncio
from main import main

PDF_FILENAME = "your_pdf.pdf"  # Make sure this file is in pdf_slack_bot/pdf directory
QUESTIONS = [
    "Your question 1?",
    "Your question 2?",
    # Add more questions as needed
]
AGENT_QUERY = "Your agent query"

asyncio.run(main(PDF_FILENAME, QUESTIONS, AGENT_QUERY))
```

## Project Structure

- `main.py`: The main script containing the core functionality
- `gui.py`: Streamlit GUI for the application
- `pdf/`: Directory containing the PDF files that can be used to generate answers
- `pdf_slack_bot/`: Directory containing the project modules
    - `utils/`: Utility functions and configurations
    - `components/`: Core components of the bot (LLM, DocumentGetter, DocumentRAG, etc.)