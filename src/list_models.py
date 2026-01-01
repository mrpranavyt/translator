import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

def translate_to_english(text: str) -> str:
    prompt = f"""
Translate the following text to English.
The text may be in Nepali or Sinhala.
Return ONLY the English translation.

Text:
{text}
"""
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text.strip()

if __name__ == "__main__":
    print("Nepali/Sinhala → English Translator (type 'exit' to quit)")
    while True:
        text = input("\nEnter text: ")
        if text.lower() == "exit":
            break
        print("English:", translate_to_english(text))
