import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

class CaseBasedReasoning:
    def __init__(self, data, categorical_cols, numeric_cols, target_col):
        self.data = data.copy()
        self.categorical_cols = categorical_cols
        self.numeric_cols = numeric_cols
        self.target_col = target_col
        self.pipeline = None
        self.transformed_data = None

    def preprocess(self):
        self.pipeline = ColumnTransformer(transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), self.categorical_cols),
            ('num', StandardScaler(), self.numeric_cols)
        ])
        self.transformed_data = self.pipeline.fit_transform(self.data)

    def predict(self, new_case, k=3):
        new_case_df = pd.DataFrame([new_case])
        new_case_transformed = self.pipeline.transform(new_case_df)

        distances = euclidean_distances(new_case_transformed, self.transformed_data)[0]
        nearest_indices = np.argsort(distances)[:k]

        similar_cases_df = pd.DataFrame([
            {**self.data.iloc[i].to_dict(), 'Distância': float(distances[i])}
            for i in nearest_indices
        ])

        target_values = self.data.iloc[nearest_indices][self.target_col].astype(float).values
        weights = 1 / (distances[nearest_indices] + 1e-6)
        predicted_value = np.average(target_values, weights=weights)

        return predicted_value, similar_cases_df
