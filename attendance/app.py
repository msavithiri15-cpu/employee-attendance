from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://employee-attendance-35543-default-rtdb.firebaseio.com/"
})

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    emp_id = request.form.get("emp_id")
    return render_template("dashboard.html", emp_id=emp_id)

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    emp_id = request.form.get("emp_id")
    status = request.form.get("status")

    today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    db.reference(f"attendance/{emp_id}/{today}").set({
        "status": status,
        "time": time_now
    })

    # 🔥 THIS LINE PREVENTS THE ERROR
    return "✅ Attendance Marked Successfully"

if __name__ == "__main__":
    app.run(debug=True)