from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pandas as pd
import joblib

def load_data(file_path, target_column):
    """
    Carrega o dataset de um arquivo CSV e separa em features e target.
    Deve ser utilizado passando o caminho do arquivo e o nome da coluna alvo.
    """
    data = pd.read_csv(file_path)
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    return X, y

def train_model(X, y):
    """
    Treina o modelo Naive Bayes e avalia sua performance.
    Retorna o modelo treinado.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Acurácia do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Matriz de confusão do modelo implantada
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Naive Bayes Confusion Matrix")
    plt.show()

    return model

def save_model(model, file_path):
    """
    Salva o modelo treinado em um arquivo usando joblib.
    Deve ser utilizado passando o modelo e o caminho do arquivo onde será salvo.
    """
    joblib.dump(model, file_path)