from flask import Flask, request, jsonify
import numpy as np
import joblib
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent / 'regression.joblib'

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

def parse_inputs(req):
    data = (req.get_json(silent=True) or {}) if req.is_json else (req.args or {})

    try:
        size = float(data.get("size"))
        bedrooms = int(data.get("bedrooms"))
        garden = int(data.get("garden"))
    except (TypeError, ValueError): raise ValueError("Wrong feature format.")

    if garden not in (0, 1): raise ValueError("Garden can only be 0 or 1.")

    return np.array([[size, bedrooms, garden]], dtype=float)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    try:
        X = parse_inputs(request)
        y_pred = float(model.predict(X)[0])
        return jsonify({"y_pred": y_pred})
    except ValueError as e: return jsonify({"error": str(e)}), 400
    except Exception as e: return jsonify({"error": f"Internal server error: {e}"}), 500

if __name__ == "__main__":
    # if someone else takes 7612 i better be damned
    app.run(host="0.0.0.0", port=7612, debug=True)
