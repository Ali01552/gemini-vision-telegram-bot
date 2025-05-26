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

### How to Set Environment Variables:

Environment variables keep sensitive information out of your code and simplify managing different credentials for various environments.

* **Linux/macOS:**
    To set them temporarily for the current terminal session:
    ```bash
    export TELEGRAM_BOT_TOKEN="your_bot_token"
    export TELEGRAM_CHAT_ID="your_chat_id"
    export GEMINI_API_KEY="your_gemini_api_key"
    python App.py
    ```
    For persistent variables, add these `export` commands to your shell's configuration file (e.g., `~/.bashrc` or `~/.zshrc`).

* **Windows (Command Prompt):**
    To set them temporarily for the current command prompt session:
    ```cmd
    set TELEGRAM_BOT_TOKEN="your_bot_token"
    set TELEGRAM_CHAT_ID="your_chat_id"
    set GEMINI_API_KEY="your_gemini_api_key"
    python App.py
    ```

* **Windows (PowerShell):**
    To set them temporarily for the current PowerShell session:
    ```powershell
    $env:TELEGRAM_BOT_TOKEN="your_bot_token"
    $env:TELEGRAM_CHAT_ID="your_chat_id"
    $env:GEMINI_API_KEY="your_gemini_api_key"
    python App.py
    ```

## Usage

```bash
python App.py [gemini-model-name]
```


## Author
### Ali Abdelbady 


