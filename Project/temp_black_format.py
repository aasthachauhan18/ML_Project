# from flask import Flask, request, render_template
# import pickle
# import numpy as np
# import os
# import json

# app = Flask(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# model_path = os.path.join(BASE_DIR, "model.pkl")
# scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
# accuracy_path = os.path.join(BASE_DIR, "accuracy.pkl")

# model = pickle.load(open(model_path, "rb"))
# scaler = pickle.load(open(scaler_path, "rb"))
# accuracy = pickle.load(open(accuracy_path, "rb"))




# @app.route('/')
# def home():
#     return render_template('index.html', accuracy=accuracy)


# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         cyl = float(request.form.get('cylinders', 0))
#         hp = float(request.form.get('horsepower', 0))
#         wt = float(request.form.get('weight', 0))
#         acc = float(request.form.get('acceleration', 0))

#         input_data = scaler.transform([[cyl, hp, wt, acc]])
#         prediction = model.predict(input_data)[0]

#         confidence = round(accuracy * 100, 2)

#         return render_template(
#             'index.html',
#             prediction=round(prediction, 2),
#             data_values=json.dumps([cyl, hp, wt, acc]),
#             accuracy=accuracy,
#             confidence=confidence   
#         )

#     except:
#         return render_template(
#             'index.html',
#             prediction="Invalid Input",
#             accuracy=accuracy
#         )



# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)





from flask import Flask, render_template, request
import pickle
from monitor import log_prediction
import numpy as np
import os
import json

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
accuracy_path = os.path.join(BASE_DIR, "accuracy.pkl")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))
accuracy = pickle.load(open(accuracy_path, "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    confidence = round(float(accuracy) * 100, 2)
    data_values = []

    if request.method == "POST":
        try:
            cylinders = float(request.form.get("cylinders", 0))
            horsepower = float(request.form.get("horsepower", 0))
            weight = float(request.form.get("weight", 0))
            acceleration = float(request.form.get("acceleration", 0))

            input_array = np.array([[cylinders, horsepower, weight, acceleration]])
            scaled_input = scaler.transform(input_array)
            result = model.predict(scaled_input)[0]

            prediction = round(float(result), 2)
            data_values = [cylinders, horsepower, weight, acceleration]

            return render_template(
                "predict.html",
                prediction=prediction,
                confidence=confidence,
                accuracy=accuracy,
                data_values=data_values
            )

        except Exception:
            return render_template(
        "predict.html",
        prediction="Invalid Input",
        confidence=confidence,
        accuracy=accuracy,
        data_values=[]
    )
    log_prediction(
    cylinders=cylinders,
    horsepower=horsepower,
    weight=weight,
    acceleration=acceleration,
    prediction=prediction
)

    return render_template(
        "predict.html",
        prediction=prediction,
        confidence=confidence,
        accuracy=accuracy,
        data_values=data_values
    )


if __name__ == "__main__":
    app.run(debug=True)