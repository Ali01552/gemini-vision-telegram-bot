# Gemini Vision Telegram Bot

This script:
- Takes a screenshot (Wayland-compatible using `grim`)
- Sends the image to Gemini Vision (Generative AI)
- Extracts and answers medical MCQ questions
- Sends the result to a Telegram chat

## Features
- Clinical MCQ analysis using Gemini
- Telegram bot integration for mobile notification
- Screenshot automation

## Requirements
- Python 3.9+
- `grim` for screenshots (Wayland only)
- Telegram Bot Token
- Gemini API key

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python App.py [gemini-model-name]
```

## Environment Variables
- Replace the hardcoded API_KEY, bot_token, and chat_id with environment variables in production.

## Author
### Ali Abdelbady 


