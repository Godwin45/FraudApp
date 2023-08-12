import numpy as np
import pandas as pd
import mlflow
import joblib
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, precision_score, recall_score, f1_score, accuracy_score
from urllib.parse import urlparse
from mlProject.entity.config_entity import ModelEvaluationConfig
from mlProject.utils.common import save_json


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        
        precision = precision_score(actual, pred)  # Precision
        recall = recall_score(actual, pred)        # Recall
        f1 = f1_score(actual, pred)                # F1-score
        accuracy = accuracy_score(actual, pred)    # Accuracy
        
        return rmse, mae, r2, precision, recall, f1, accuracy

    def log_into_mlflow(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1).values
        test_y = test_data[[self.config.target_column]].values.ravel()

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2, precision, recall, f1, accuracy) = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
            scores = {
                "rmse": rmse, "mae": mae, "r2": r2,
                "precision": precision, "recall": recall, "f1": f1, "accuracy": accuracy
            }
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("accuracy", accuracy)

            # Model registry does not work with the file store
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="FraudAppModel")
            else:
                mlflow.sklearn.log_model(model, "model")
