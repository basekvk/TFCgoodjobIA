import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import logging
import os

logging.basicConfig(level=logging.INFO)

def train_model():
    try:
        # Verifica que el archivo exista
        file_path = os.path.join('data', 'UNSW_NB15.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no fue encontrado.")
        
        logging.info(f"Cargando datos desde {file_path}")
        # Cargar el dataset UNSW-NB15 con manejo de tipos mixtos
        df = pd.read_csv(file_path, low_memory=False)
        
        # Verifica si las columnas 'label' y 'attack_cat' existen
        if 'label' not in df.columns or 'attack_cat' not in df.columns:
            raise KeyError("Las columnas 'label' y 'attack_cat' no se encontraron en el archivo CSV")
        
        # Seleccionar una muestra del conjunto de datos
        df_sample = df.sample(frac=0.1, random_state=42)  # Utilizar solo el 10% de los datos para entrenar

        # Seleccionar características y etiquetas
        X = df_sample.drop(['label', 'attack_cat'], axis=1)
        y = df_sample['label']
        
        # Identificar las columnas categóricas
        categorical_cols = [cname for cname in X.columns if X[cname].dtype == "object"]
        numeric_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]
        
        # Guardar las columnas utilizadas durante el entrenamiento
        joblib.dump(X.columns, 'models/train_columns.pkl')
        
        # Preprocesamiento para variables numéricas y categóricas
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median'))
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Ajustar el preprocesador con los datos de entrenamiento
        preprocessor.fit(X_train)
        
        # Preprocesar los datos de entrenamiento
        X_train = preprocessor.transform(X_train)
        X_test = preprocessor.transform(X_test)

        # Definir el modelo y los hiperparámetros a probar
        model = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [50, 100],  # Reducir el número de estimadores
            'max_depth': [None, 10],  # Reducir la profundidad máxima
            'min_samples_split': [2, 5],  # Menos combinaciones de hiperparámetros
            'min_samples_leaf': [1, 2]
        }

        # Configurar la búsqueda de hiperparámetros
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

        # Entrenar el modelo
        grid_search.fit(X_train, y_train)

        # Obtener el mejor modelo
        best_model = grid_search.best_estimator_

        # Evaluar el modelo
        y_pred = best_model.predict(X_test)
        logging.info(f"Precisión: {accuracy_score(y_test, y_pred)}")
        logging.info(f"Informe de clasificación:\n {classification_report(y_test, y_pred)}")
        logging.info(f"Matriz de confusión:\n {confusion_matrix(y_test, y_pred)}")

        # Guardar el modelo entrenado y el preprocesador ajustado
        joblib.dump(best_model, os.path.join('models', 'ids_model_unws_nb15.pkl'))
        joblib.dump(preprocessor, os.path.join('models', 'preprocessor.pkl'))
        logging.info("Modelo y preprocesador guardados exitosamente.")
    except FileNotFoundError as e:
        logging.error(f"Archivo de datos no encontrado: {e}")
    except KeyError as e:
        logging.error(f"Error en el archivo CSV: {e}")
    except Exception as e:
        logging.error(f"Error entrenando el modelo: {e}")

if __name__ == "__main__":
    train_model()
