from groq import Groq
import os
from config import GROQ_API_KEY, MODEL_NAME

def ask_llm(messages):
    client = Groq(api_key=GROQ_API_KEY)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()
