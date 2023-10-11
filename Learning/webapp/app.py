import os
import swimclub
from flask import Flask, session, render_template

app = Flask(__name__)
app.secret_key = "You will never guss..."

@app.get("/")
def index():
    return render_template(
        "index.html",
        title="Welcome to the Swimclub system",
    )

def populate_data():
    if "swimmers" not in session:
        swim_files = os.listdir(swimclub.FOLDER)
        swim_files.remove(".DS_Store")
        session["swimmers"] = {}
        for file in swim_files:
            name, *_ = swimclub.read_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)

@app.get("/swimmers")
def display_swimmers():
    populate_data()
    return str(sorted(session["swimmers"]))

@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])

if __name__ == "__main__":
    app.run(debug=True)