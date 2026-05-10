import subprocess
import os
import sys
import asyncio
import tempfile
import pyautogui  # Replacement for grim (Install via: pip install pyautogui)
from PIL import Image
import google.generativeai as genai
from telegram import Bot

# --- Environment Variables ---
# Make sure these are set in your Windows Environment Variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN") 
chatid = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("GEMINI_API_KEY")

if not all([bot_token, chatid, API_KEY]):
    print("Error: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, and GEMINI_API_KEY must be set.")
    sys.exit(1)

async def send_telegram_message(message, image_path=None):
    try:
        bot = Bot(token=bot_token)
        if image_path:
            with open(image_path, 'rb') as f:
                await bot.send_photo(chat_id=chatid, photo=f, caption=message)
        else:
            await bot.send_message(chat_id=chatid, text=message)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

# === CONFIGURATION ===
# Using gemini-1.5-flash: Best balance of speed/intelligence for the free tier
MODEL_NAME = sys.argv[1] if len(sys.argv) > 1 else "gemini-1.5-flash"

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def take_screenshot():
    """Takes a screenshot using pyautogui (Windows compatible)."""
    try:
        # Save to a temporary directory
        temp_dir = tempfile.gettempdir()
        screenshot_path = os.path.join(temp_dir, "gemini_screenshot.png")
        
        # Take the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        error_msg = f"Failed to take screenshot on Windows: {e}"
        print(error_msg)
        asyncio.run(send_telegram_message(error_msg))
        sys.exit(1)

def ask_gemini_vision(image_path):
    """Send image to Gemini model and return response."""
    gemini_prompt = (
        "You are a professional AI assistant trained in clinical pharmacy, medical sciences, "
        "and medical regulations in Egypt. Analyze the MCQ in this image.\n\n"
        "1. Extract the text accurately.\n"
        "2. Identify the correct answer using evidence-based references (FDA, BNF, UpToDate, Lexicomp, EDA).\n"
        "3. Format your response exactly like this:\n"
        "   The correct answer is [Option Letter]) [Option Text]\n\n"
        "If unclear, state: 'Unable to extract or analyze the question clearly.'"
    )

    try:
        img = Image.open(image_path)
        # Gemini 1.5 models use generate_content for both text and images
        response = model.generate_content([gemini_prompt, img])
        return response.text
    except Exception as e:
        error_msg = f"Gemini API Error: {e}"
        asyncio.run(send_telegram_message(error_msg))
        return error_msg

def main():
    image_path = take_screenshot()
    result = ask_gemini_vision(image_path)
    
    # Prepend the model name for tracking
    message_to_send = f"Model: {MODEL_NAME}\n\n{result}"
    
    asyncio.run(send_telegram_message(message_to_send, image_path))
    
    # Optional: Clean up the screenshot file after sending
    if os.path.exists(image_path):
        os.remove(image_path)

if __name__ == "__main__":
    main()
