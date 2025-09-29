import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

C = 1.0
max_iter = 200

mlflow.set_tracking_uri("http://127.0.0.1:5000")

with mlflow.start_run():
    mlflow.log_param("C", C)
    mlflow.log_param("max_iter", max_iter)

    model = LogisticRegression(C=C, max_iter=max_iter)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mlflow.log_metric("accuracy", acc)

    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="model",
        input_example=X_train[:1]
    )    

    print(f"Accuracy: {acc}")

