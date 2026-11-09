"""Feature engineering for academic performance prediction"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any


class AcademicFeatureEngineer:
    """Engineer features for academic performance prediction"""

    def __init__(self):
        self.feature_names = []

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer all features from raw data"""
        features = df.copy()

        # Attendance features
        if 'sessions_attended' in features.columns and 'sessions_scheduled' in features.columns:
            features['attendance_rate'] = features['sessions_attended'] / features['sessions_scheduled'].replace(0, np.nan)
            features['attendance_rate'] = features['attendance_rate'].fillna(0)

        # LMS engagement features
        if 'logins_count' in features.columns:
            features['lms_engagement'] = features['logins_count'] / features.get('weeks', 1)
            features['lms_engagement'] = features['lms_engagement'].fillna(0)

        # Assessment features
        if 'assessment_marks' in features.columns:
            features['mean_assessment_mark'] = features['assessment_marks'].apply(lambda x: np.mean(x) if isinstance(x, list) else x)
            features['assessment_trend'] = features.get('assessment_trend', 0)

        # Course load features
        if 'credits' in features.columns and 'previous_gpa' in features.columns:
            features['credit_gpa_ratio'] = features['credits'] / (features['previous_gpa'] + 0.1)

        # Interaction features
        if 'attendance_rate' in features.columns and 'lms_engagement' in features.columns:
            features['engagement_index'] = (features['attendance_rate'] + features['lms_engagement']) / 2

        self.feature_names = [col for col in features.columns if col not in ['student_id', 'outcome', 'pass/fail']]
        return features

    def get_feature_names(self) -> List[str]:
        """Get list of engineered feature names"""
        return self.feature_names