import mlflow
import mlflow.sklearn
import pandas as pd
mlflow.set_experiment("first_experiment")

    
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import datasets
data = datasets.load_iris()

df = pd.DataFrame(data=data.data, columns=data.feature_names)
df['target'] = data.target

X = df.drop("target", axis=1)
y = df["target"] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)

input_example = X_test.iloc[0].to_dict()

with mlflow.start_run():
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(model, "model", input_example=input_example)

print(f"error: {mse}")