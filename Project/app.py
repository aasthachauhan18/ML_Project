from flask import Flask, request, render_template
import pickle
import numpy as np
import os
import json

app = Flask(__name__)

# 🔹 Get current directory (fix file path issues)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 Load model and scaler safely
model_path = os.path.join(BASE_DIR, "model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
accuracy_path = os.path.join(BASE_DIR, "accuracy.pkl")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))
accuracy = pickle.load(open(accuracy_path, "rb"))

# 🔹 Model accuracy (replace with your real value from notebook)
# accuracy = 0.87


# ✅ Home route
@app.route('/')
def home():
    return render_template('index.html', accuracy=accuracy)


# ✅ Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        cyl = float(request.form.get('cylinders', 0))
        hp = float(request.form.get('horsepower', 0))
        wt = float(request.form.get('weight', 0))
        acc = float(request.form.get('acceleration', 0))

        input_data = scaler.transform([[cyl, hp, wt, acc]])
        prediction = model.predict(input_data)[0]

        # ✅ ADD THIS LINE HERE
        confidence = round(accuracy * 100, 2)

        # ✅ RETURN (IMPORTANT: pass confidence)
        return render_template(
            'index.html',
            prediction=round(prediction, 2),
            data_values=json.dumps([cyl, hp, wt, acc]),
            accuracy=accuracy,
            confidence=confidence   # ✅ pass to HTML
        )

    except:
        return render_template(
            'index.html',
            prediction="Invalid Input",
            accuracy=accuracy
        )


# ✅ Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)