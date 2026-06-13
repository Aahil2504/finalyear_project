from flask import Flask, render_template, request
import subprocess
import sys
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    name = request.form["name"].strip().replace(" ", "_")

    script_path = os.path.join("src", "register_face.py")

    # Open camera in a separate process (NON-BLOCKING)
    subprocess.Popen(
        [sys.executable, script_path, name],
        shell=True
    )

    return f"""
    <h2>Camera opened for {name}</h2>
    <p>Please look at the camera. Face registration in progress.</p>
    <p>You can close the camera window when done.</p>
    <a href="/">Go back</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
