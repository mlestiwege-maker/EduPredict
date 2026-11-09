"""Model training and evaluation"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Train and evaluate multiple models for academic performance prediction"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()

    def initialize_models(self) -> Dict[str, Any]:
        """Initialize candidate models"""
        self.models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=self.random_state
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=5,
                random_state=self.random_state
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=self.random_state
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=self.random_state
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=self.random_state,
                use_label_encoder=False,
                eval_metric='logloss'
            ),
        }
        return self.models

    def train_model(self, model_name: str, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """Train a specific model"""
        model = self.models[model_name]
        model.fit(X_train, y_train)
        return model

    def evaluate_model(self, model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
        }

        if y_prob is not None:
            metrics['roc_auc'] = roc_auc_score(y_test, y_prob)

        return metrics

    def cross_validate_model(self, model_name: str, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]:
        """Perform cross-validation"""
        model = self.models[model_name]
        scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
        return {
            'mean_f1': scores.mean(),
            'std_f1': scores.std(),
            'scores': scores.tolist()
        }

    def train_and_evaluate_all(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Dict[str, float]]:
        """Train and evaluate all models"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        results = {}
        for model_name in self.models:
            print(f"Training {model_name}...")
            model = self.train_model(model_name, X_train_scaled, y_train)
            metrics = self.evaluate_model(model, X_test_scaled, y_test)
            results[model_name] = metrics
            print(f"  {model_name} - F1: {metrics['f1']:.3f}, Recall: {metrics['recall']:.3f}")

        return results

    def get_best_model(self, results: Dict[str, Dict[str, float]], metric: str = 'f1') -> str:
        """Get the best performing model based on a metric"""
        best_model = max(results.items(), key=lambda x: x[1].get(metric, 0))
        return best_model[0]