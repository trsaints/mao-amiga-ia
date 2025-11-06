import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import euclidean

class CaseBasedReasoning:
    def __init__(self, data: pd.DataFrame, categorical_cols, numeric_cols, target_col):
        """
        data: DataFrame com os casos
        categorical_cols: lista de colunas categóricas
        numeric_cols: lista de colunas numéricas
        target_col: nome da coluna de saída (ex: 'valor_total')
        """
        self.data = data.copy()
        self.categorical_cols = categorical_cols
        self.numeric_cols = numeric_cols
        self.target_col = target_col
        self.scaler = MinMaxScaler()
        self.df_processed = None

    def preprocess(self):
        """Transforma categorias e normaliza os dados"""
        df = pd.get_dummies(self.data, columns=self.categorical_cols)
        df[self.numeric_cols] = self.scaler.fit_transform(df[self.numeric_cols])
        self.df_processed = df
        return df

    def compute_similarity(self, new_case):
        """Calcula a similaridade (distância euclidiana) entre o novo caso e os existentes"""
        if self.df_processed is None:
            raise ValueError("Execute preprocess() antes de calcular similaridade.")
        
        new_df = pd.DataFrame([new_case])
        new_df = pd.get_dummies(new_df, columns=self.categorical_cols)
        
        for col in self.df_processed.columns:
            if col not in new_df:
                new_df[col] = 0
        new_df = new_df[self.df_processed.columns]

        new_df[self.numeric_cols] = self.scaler.transform(new_df[self.numeric_cols])
        
        distances = []
        for i, row in self.df_processed.iterrows():
            dist = euclidean(new_df.iloc[0].values, row.values)
            distances.append((i, dist))
        
        return sorted(distances, key=lambda x: x[1])

    def predict(self, new_case, k=3):
        """Prevê o valor total com base nos k casos mais parecidos"""
        distances = self.compute_similarity(new_case)
        k_nearest = distances[:k]
        similar_cases = self.data.iloc[[i for i, _ in k_nearest]]
        predicted_value = similar_cases[self.target_col].mean()

        return predicted_value, similar_cases
