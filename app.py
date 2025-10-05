from flask import Flask, request, render_template
import logo_gen

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        forma = request.form.get("forma")
        style = request.form.get("style")
        description = request.form.get("description")

        result = logo_gen.generate_logo(forma, style, description)

        if not result["success"]:
            return render_template("index.html", error=result["error"])
        return render_template("index.html", image=result["path"])

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)