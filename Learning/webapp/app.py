import os
import swimclub
from flask import Flask, session, render_template, request

app = Flask(__name__)
app.secret_key = "You will never guess..."

@app.get("/")
def index():
    return render_template(
        "index.html",
        title="‿︵‿︵‿︵‿︵‿︵‿︵Welcome to Swimclub ‿︵‿︵‿︵‿︵‿︵‿︵‿",
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
    return render_template(
        "select.html",
        title="Choose Your Swimmer!",
        url="/showfiles",
        select_id="swimmer",
        data=sorted(session["swimmers"]),
    )

@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])

@app.post("/showfiles")
def display_swimmer_files():
    populate_data()
    name = request.form["swimmer"]
    return render_template(
        "select.html",
        title="Choose Your Battle!",
        url="/showbarchart",
        select_id="file",
        data=session["swimmers"][name],
    )

@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"]
    location = swimclub.produce_bar_chart(file_id, "templates/")
    return render_template(location.split("/")[-1])

if __name__ == "__main__":
    app.run(debug=True)