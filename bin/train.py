"""Script to train and save model"""
import os
from typing import Any, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn import datasets, ensemble
from sklearn.model_selection import train_test_split

from utils import utils

MODEL_NAME = os.environ.get("MODEL_NAME", "randomforest")
MODEL_ARTIFACT = f"outputs/{MODEL_NAME}.pkl"


def load_data() -> Tuple[pd.DataFrame]:
    """Load Iris dataset

    Returns:
        Tuple[pd.DataFrame]: Feature matrix and label vector
    """
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    return X, y


def split_data(X: pd.DataFrame, y: pd.Series) -> Tuple[np.array]:
    """Split data into train and test split"""
    return train_test_split(X, y, random_state=123)


def train_model(X: pd.DataFrame, y: pd.Series) -> Any:
    """Train RandomForest model

    Args:
        X (pd.DataFrame): feature matrix
        y (pd.Series): label vector

    Returns:
        [type]: trained model
    """
    model = ensemble.RandomForestClassifier(random_state=123)
    model.fit(X, y)
    return model


def save_model(model: Any, path: str) -> None:
    """Serialize trained model

    Args:
        model (Any): trained model instance
        path (str): path to model artifact
    """
    utils.setup_file(path, overwrite=True)
    joblib.dump(model, open(path, 'wb'))
    # TODO: push to s3


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X=X, y=y)
    model = train_model(X=X_train, y=y_train)
    predictions = model.predict(X_test)
    print(f"Train score: {model.score(X_train, y_train)}")
    print(f"Test score: {model.score(X_test, y_test)}")
    save_model(model=model, path=MODEL_ARTIFACT)


if __name__ == "__main__":
    main()
