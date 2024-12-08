from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML Template
template = """
<!doctype html>
<html>
    <head>
        <title>Protein Intake Calculator</title>
    </head>
    <body>
        <h1>Protein Intake Calculator</h1>
        <p>Enter your details to calculate your daily protein requirements.</p>
        <form method="post">
            <label for="height">Height (in feet and inches, e.g., 5'7"): </label>
            <input type="text" name="height" required><br><br>
            <label for="weight">Weight (in kg): </label>
            <input type="number" name="weight" required><br><br>
            <label for="bodyfat">Body Fat Percentage (optional): </label>
            <input type="number" name="bodyfat" step="0.1"><br><br>
            <button type="submit">Calculate</button>
        </form>
        {% if result %}
        <h2>Results</h2>
        <p>Protein requirements with resistance training: <b>{{ result['with_training'] }} grams/day</b></p>
        <p>Protein requirements without resistance training: <b>{{ result['without_training'] }} grams/day</b></p>
        <h3>References</h3>
        <ul>
            <li><a href="https://doi.org/10.1186/s40798-022-00508-w" target="_blank">2022 Study: Protein and Muscle Strength</a></li>
            <li><a href="https://doi.org/10.1093/nutrit/nuaa104" target="_blank">2020 Study: Protein and Lean Body Mass</a></li>
        </ul>
        {% endif %}
    </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            # Get inputs
            height = request.form["height"]
            weight = float(request.form["weight"])
            bodyfat = request.form.get("bodyfat", None)
            bodyfat = float(bodyfat) if bodyfat else None

            # Calculate lean body mass if body fat is provided
            lean_mass = weight * (1 - (bodyfat / 100)) if bodyfat else None

            # Protein calculations
            with_training = round(weight * 1.5, 2)  # 1.5 g/kg BW/day
            without_training = round(weight * 1.3, 2)  # 1.3 g/kg BW/day

            result = {
                "with_training": with_training,
                "without_training": without_training,
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template_string(template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
