import config
from modules.llm_client import ask_llm
from modules.conversation_logger import get_recent_history

def generate_response(user_message, user_id=None):
    try:
        # Get recent history for context memory (increased to 6 for better recall)
        history = get_recent_history(user_id=user_id, limit=6)
        
        # Build messages list
        messages = [{"role": "system", "content": config.SYSTEM_PROMPT + "\nAt the very end of your response, add: [Mood: <mood>] [Category: <category>]"}]
        
        if history:
            messages.append({"role": "system", "content": "--- CONVERSATION HISTORY ---"})
            messages.extend(history)
            messages.append({"role": "system", "content": "--- CURRENT USER MESSAGE BELOW ---"})
            
        messages.append({"role": "user", "content": user_message})
        
        full_reply = ask_llm(messages)
        
        # Extract mood and category
        mood = "Neutral"
        category = "General"
        
        if "[Mood:" in full_reply:
            parts = full_reply.split("[Mood:")
            reply_text = parts[0].strip()
            meta_parts = parts[1].split("]")
            mood = meta_parts[0].strip()
            if "[Category:" in parts[1]:
                category = parts[1].split("[Category:")[1].split("]")[0].strip()
        else:
            reply_text = full_reply

        return {"reply": reply_text, "mood": mood, "category": category}
    except Exception as e:
        # This will print the error in the terminal
        print("\n--- LLM ERROR ---")
        print(f"Details: {e}")
        print("---------------------\n")
        
        error_msg = str(e).lower()
        if "rate_limit" in error_msg:
            return {"reply": "Error: Rate limit reached. Please wait a moment.", "mood": "Neutral", "category": "Error"}
        elif "authentication" in error_msg or "invalid_api_key" in error_msg:
            return {"reply": "Error: The API key provided is invalid. Please check your .env file.", "mood": "Neutral", "category": "Error"}
        else:
            return {"reply": f"I'm sorry, I encountered an error: {e}", "mood": "Neutral", "category": "Error"}