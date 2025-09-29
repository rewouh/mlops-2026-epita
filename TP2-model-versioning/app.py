from flask import Flask, request, jsonify
import mlflow.pyfunc
import mlflow
import random

app = Flask(__name__)

current_model = None
next_model = None
model_name = "model"
current_version = 1
next_version = 1
p = 0.8

def load_model_from_mlflow(name, version):
    uri = f"models:/{name}/{version}"
    return mlflow.pyfunc.load_model(uri)

mlflow.set_tracking_uri("http://127.0.0.1:5000")
current_model = load_model_from_mlflow(model_name, current_version)
next_model = load_model_from_mlflow(model_name, next_version)
print(f"Loaded current={model_name} v{current_version}, next={model_name} v{next_version}")

@app.route("/predict", methods=["POST"])
def predict():
    global current_model, next_model, p
    data = request.get_json()
    if not data or "inputs" not in data:
        return jsonify({"error": "inputs is required"}), 400

    try:
        if random.random() < p:
            model_used = "current"
            preds = current_model.predict(data["inputs"]).tolist()
        else:
            model_used = "next"
            preds = next_model.predict(data["inputs"]).tolist()
        return jsonify({"predictions": preds, "model_used": model_used})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-model", methods=["POST"])
def update_model():
    global next_model, next_version
    data = request.get_json()
    if not data or "version" not in data:
        return jsonify({"error": "version is required"}), 400
    try:
        version = int(data["version"])
        next_model = load_model_from_mlflow(model_name, version)
        next_version = version
        return jsonify({"status": f"model updated to {version}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/accept-next-model", methods=["POST"])
def accept_next_model():
    global current_model, next_model, current_version, next_version
    try:
        current_model = next_model
        current_version = next_version
        return jsonify({"status": f"next model is now current, with version {current_version}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001) 
