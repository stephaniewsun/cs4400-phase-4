from flask import Flask, render_template

app = Flask(__name__)

@app.route("/add_person", methods=["GET"])
def add_person():
    return render_template("add_person.html")

if __name__ == "__main__":
    app.run(debug=True)
