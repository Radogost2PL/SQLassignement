from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def contact():
    submitted_name = None
    if request.method == "POST":
        submitted_name = request.form.get("user_name")

    return render_template("form.html", name=submitted_name)


if __name__ == "__main__":
    app.run(debug=True)