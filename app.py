from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import engine

app = Flask(__name__)
app.secret_key = "replace-this-with-random"
app.permanent_session_lifetime = timedelta(hours=6)

def _get_state():
    if "state" not in session:
        session["state"] = engine.initial_state()
    if "history" not in session:
        session["history"] = []
    return session["state"], session["history"]

def _set_state(state, history):
    session["state"] = state
    session["history"] = history

@app.route("/", methods=["GET", "POST"])
def index():
    state, history = _get_state()
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        out, state = engine.step(state, user_input)
        if user_input.strip():
            history.append({"role": "user", "text": user_input})
        if out:
            history.append({"role": "system", "text": out})
        _set_state(state, history)
        return redirect(url_for("index"))
    if not history:
        out, state = engine.step(state, "")
        if out:
            history.append({"role": "system", "text": out})
        _set_state(state, history)
    return render_template("index.html", history=history)

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
