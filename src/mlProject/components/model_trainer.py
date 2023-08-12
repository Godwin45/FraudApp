import pandas as pd
import os
from mlProject import logger
from sklearn.linear_model import ElasticNet
import joblib
from mlProject.entity.config_entity import ModelTrainerConfig
import pandas as pd
from mlProject import logger
import joblib
# Classifier Libraries
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        X_train = train_x.values
        X_test = test_x.values
        y_train = train_y.values.ravel()
        y_test = test_y.values.ravel()

        classifiers = {
            "LogisticRegression": LogisticRegression(),
            "KNearest": KNeighborsClassifier(),
            "SupportVectorClassifier": SVC(),
            "DecisionTreeClassifier": DecisionTreeClassifier()
        }

        best_accuracy = 0.0
        best_model = None

        for classifier_name, classifier in classifiers.items():
            classifier_params = self.config.classifier_params.get(classifier_name)
            
            if classifier_params:
                grid_classifier = GridSearchCV(classifier, classifier_params)
                grid_classifier.fit(X_train, y_train)
                best_classifier = grid_classifier.best_estimator_

                training_score = cross_val_score(best_classifier, X_train, y_train, cv=5)
                accuracy = round(training_score.mean(), 2) * 100
                print("Classifier:", classifier_name, "has a training score of", accuracy, "% accuracy score")

                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = best_classifier

        if best_model is not None:
            model_path = os.path.join(self.config.root_dir, self.config.model_name)
            joblib.dump(best_model, model_path)
            print("Best model saved with accuracy:", best_accuracy, "%")
        else:
            print("No best model found.")

        return best_model