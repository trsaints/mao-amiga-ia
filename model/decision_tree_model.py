from machine_learning_model import MachineLearningModel
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, f1_score
import matplotlib.pyplot as plt
import pandas as pd
import joblib

class DecisionTreeModel(MachineLearningModel):
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)

    def load_data(self, file_path, target_column):
        """
        Carrega os dados de um arquivo CSV e separa em variáveis independentes (X) e alvo (y).

        Parâmetros:
        - file_path (str): Caminho para o arquivo CSV contendo os dados.
        - target_column (str): Nome da coluna que representa o rótulo (classe) a ser prevista.

        Retorna:
        - None. Os dados são armazenados nos atributos self.X e self.y.
        """
        data = pd.read_csv(file_path)
        self.X = data.drop(target_column, axis=1)
        self.y = data[target_column]

    def train(self):
        """
        Realiza a divisão dos dados em treino e teste, e treina o modelo Decision Tree com os dados de treino.

        Retorna:
        - None. O modelo treinado é armazenado em self.model.
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        """
        Avalia o desempenho do modelo nos dados de teste.

        Exibe:
        - Acurácia
        - Precisão (média ponderada)
        - F1 Score (média ponderada)
        - Matriz de confusão

        Retorna:
        - None.
        """
        y_pred = self.model.predict(self.X_test)

        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted')
        f1 = f1_score(self.y_test, y_pred, average='weighted')

        print(f'Acurácia: {accuracy * 100:.2f}%')
        print(f'Precisão: {precision * 100:.2f}%')
        print(f'F1 Score: {f1 * 100:.2f}%')

        cm = confusion_matrix(self.y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        plt.title(f"{self.__class__.__name__} - Matriz de Confusão")
        plt.show()


    def save_model(self, file_path):
        """
        Salva o modelo treinado em um arquivo utilizando a biblioteca joblib.

        Parâmetros:
        - file_path (str): Caminho do arquivo onde o modelo será salvo.

        Retorna:
        - None.
        """
        joblib.dump(self.model, file_path)
