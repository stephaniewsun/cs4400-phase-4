from flask import Flask, render_template
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

@app.route("/add_person", methods=["GET"])
def add_person():
    return render_template("add_person.html")

if __name__ == "__main__":
    app.run(debug=True)
