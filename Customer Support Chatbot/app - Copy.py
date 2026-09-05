from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from modules.response_engine import generate_response
from modules.conversation_logger import (
    log_chat, create_ticket, save_feedback, 
    init_db, create_user, verify_user, get_chat_history,
    delete_chat, clear_all_history
)
from modules.escalation import needs_escalation
import os
import traceback

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize database
init_db()

@app.route("/")
def home():
    if 'user_id' in session:
        return redirect(url_for('chat_page'))
    return render_template("welcome.html")

@app.route("/chat_page")
def chat_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("chat.html", username=session.get('username'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            data = request.json
            uid = verify_user(data['username'], data['password'])
            if uid:
                session['user_id'] = uid
                session['username'] = data['username']
                return jsonify({"status": "success"})
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return render_template("chat.html", auth_mode="login")

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        if create_user(data['username'], data['password']):
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Username already taken"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/history")
def history():
    if 'user_id' not in session:
        return jsonify([])
    try:
        data = get_chat_history(session['user_id'])
        return jsonify(data if data else [])
    except:
        return jsonify([])

@app.route("/delete_chat", methods=["POST"])
def remove_chat():
    if 'user_id' not in session:
        return jsonify({"status": "error"}), 401
    chat_id = request.json.get("id")
    delete_chat(chat_id, session['user_id'])
    return jsonify({"status": "success"})

@app.route("/clear_history", methods=["POST"])
def clear_history():
    if 'user_id' not in session:
        return jsonify({"status": "error"}), 401
    clear_all_history(session['user_id'])
    return jsonify({"status": "success"})

@app.route("/chat", methods=["POST"])
def chat():
    if 'user_id' not in session:
        return jsonify({"reply": "Unauthorized. Please log in again.", "error": True}), 401
        
    try:
        user_id = session['user_id']
        user_message = request.json.get("message", "").strip()
        
        if not user_message:
            return jsonify({"reply": "Please type something. 😊"})

        # Simple Trigger for Human Handover
        if "human" in user_message.lower() or "agent" in user_message.lower() or "support" in user_message.lower():
            reply = "Handing you over to a live agent... Please wait. 🎧"
            log_chat(user_message, reply, user_id=user_id, mood="Neutral", category="Support")
            return jsonify({"reply": reply, "action": "handover"})

        if needs_escalation(user_message):
            ticket_id = create_ticket(user_message, user_id=user_id, category="Escalation")
            reply = f"This seems serious. I've created a support ticket (#TK{ticket_id}) for you. A human agent will follow up soon. 🎫"
            log_chat(user_message, reply, user_id=user_id, mood="Angry", category="Escalation")
            return jsonify({"reply": reply})
        else:
            res = generate_response(user_message, user_id=user_id)
            reply = res.get("reply", "I'm sorry, I couldn't generate a response.")
            log_chat(user_message, reply, user_id=user_id, mood=res.get("mood", "Neutral"), category=res.get("category", "General"))
            return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERROR IN CHAT ROUTE: {traceback.format_exc()}")
        return jsonify({"reply": f"I encountered an error. Please try again. ({str(e)})"}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        save_feedback(data["rating"], user_id=session['user_id'], comment=data.get("comment", ""))
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
