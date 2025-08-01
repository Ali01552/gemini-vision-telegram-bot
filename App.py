import subprocess
import os
import sys
from PIL import Image
import google.generativeai as genai
from telegram import Bot, InputFile
import asyncio

# --- Environment Variables ---
bot_toket = os.getenv("TELEGRAM_BOT_TOKEN") 
chatid = os.getenv("TELEGRAM_CHAT_ID")

if not bot_toket or not chatid:
    print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
    sys.exit(1)

async def send_telegram_message(message, image_path=None):
    try:
        bot = Bot(token=bot_toket)
        if image_path:
            with open(image_path, 'rb') as f:
                await bot.send_photo(chat_id=chatid, photo=InputFile(f), caption=message)
        else:
            await bot.send_message(chat_id=chatid, text=message)
    except Exception as e:
        print("Failed to send Telegram message:", e)

# === CONFIGURATION ===
API_KEY = os.getenv("GEMINI_API_KEY") 
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable must be set.")
    sys.exit(1)

MODEL_NAME = sys.argv[1] if len(sys.argv) > 1 else "gemini-2.0-flash"
SCREENSHOT_PATH = os.path.expanduser("~/Screenshots/gemini_screenshot.png")
OUTPUT_DIR = os.path.dirname(SCREENSHOT_PATH)

# Initialize Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def take_screenshot():
    """Takes a screenshot using grim (Wayland compatible)."""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        subprocess.run(["grim", SCREENSHOT_PATH], check=True)
        return SCREENSHOT_PATH
    except subprocess.CalledProcessError as e:
        asyncio.run(send_telegram_message(f"Failed to take screenshot with grim: {e}"))
        sys.exit(1)

def ask_gemini_vision(image_path):
    """Send image to Gemini model and return response."""
    gemini_prompt = (
    "You are a professional AI assistant trained in clinical pharmacy, medical sciences and medical regulations in Egypt "
    "I will provide you a screenshot containing a multiple-choice question (MCQ).\\n\\n"
    "Your task is to:\\n"
    "1. Extract the text from the screenshot accurately.\\n"
    "2. Understand the context of the question.\\n"
    "3. Identify the correct answer using up-to-date, evidence-based, and reliable references such as FDA guidelines, BNF, UpToDate, Lexicomp, or clinical practice guidelines and Egyptian Drug Authority.\\n"
    "4. Return the correct option letter and text only in the following format:\\n\\n"
    "    The correct answer is [Option Letter]) [Option Text]\\n\\n"
    "If the question is unclear or the image is unreadable, say:\\n"
    "    'Unable to extract or analyze the question clearly. Please provide a higher quality image.'\\n\\n"
    "Begin when I upload the screenshot."
)

    try:
        img = Image.open(image_path)
        response = model.generate_content([gemini_prompt, img])
        return response.text
    except Exception as e:
        asyncio.run(send_telegram_message(f"Gemini Error: {e}"))
        return f"Error with Gemini: {e}"

def main():
    image_path = take_screenshot()
    result = ask_gemini_vision(image_path)
    message_to_send = f'{MODEL_NAME}\n{result}'
    asyncio.run(send_telegram_message(message_to_send))

if __name__ == "__main__":
    main()
