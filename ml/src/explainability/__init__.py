"""Model explainability using SHAP"""

import shap
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Tuple


class ModelExplainer:
    """Explain model predictions using SHAP"""

    def __init__(self, model: Any, X_train: pd.DataFrame):
        self.model = model
        self.X_train = X_train
        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self):
        """Initialize SHAP explainer"""
        try:
            if hasattr(self.model, 'feature_importances_'):
                # Tree-based models
                self.explainer = shap.TreeExplainer(self.model)
            else:
                # Other models - use KernelExplainer with background data
                background = shap.sample(self.X_train, 100)
                self.explainer = shap.KernelExplainer(self.model.predict_proba, background)
        except Exception as e:
            print(f"Warning: Could not initialize SHAP explainer: {e}")
            self.explainer = None

    def explain_prediction(self, X_instance: pd.DataFrame) -> List[Dict[str, Any]]:
        """Explain a single prediction"""
        if self.explainer is None:
            return []

        try:
            shap_values = self.explainer.shap_values(X_instance)

            # Handle different SHAP value formats
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # For binary classification, use positive class
            if isinstance(shap_values, np.ndarray) and len(shap_values.shape) > 2:
                shap_values = shap_values[0]

            explanations = []
            for i, (feature, shap_value) in enumerate(zip(X_instance.columns, shap_values[0])):
                explanations.append({
                    'feature': feature,
                    'value': float(X_instance.iloc[0][feature]),
                    'shap_value': float(shap_value),
                    'impact': 'positive' if shap_value > 0 else 'negative',
                    'abs_impact': abs(float(shap_value))
                })

            # Sort by absolute impact
            explanations.sort(key=lambda x: x['abs_impact'], reverse=True)
            return explanations

        except Exception as e:
            print(f"Warning: Could not explain prediction: {e}")
            return []

    def get_global_importance(self) -> Dict[str, float]:
        """Get global feature importance"""
        if self.explainer is None:
            return {}

        try:
            shap_values = self.explainer.shap_values(self.X_train)

            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            if isinstance(shap_values, np.ndarray) and len(shap_values.shape) > 2:
                shap_values = shap_values[:, :, 1]

            importance = np.abs(shap_values).mean(axis=0)
            feature_importance = dict(zip(self.X_train.columns, importance))
            return feature_importance

        except Exception as e:
            print(f"Warning: Could not get global importance: {e}")
            return {}