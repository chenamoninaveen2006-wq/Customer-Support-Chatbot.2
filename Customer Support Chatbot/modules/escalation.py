def needs_escalation(message):
    negative_words = [
        "angry", "worst", "fraud", "cheated", "terrible", "complaint", "scam",
        "worst service", "bad experience",
        "ಕೋಪ", "మోసం", "న్యాయం", "ఫ్రాడ్", "చెత్త", # Telugu keywords
        "धोखा", "बेकार", "गुस्सा", "शिकायत", "खराब"    # Hindi keywords
    ]
    msg = message.lower()

    return any(word in msg for word in negative_words)