# Importar librerías

import pandas as pd
import numpy as np

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import (
    LinearRegression,
    Ridge
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.neighbors import (
    KNeighborsRegressor
)

from sklearn.svm import SVR

from sklearn.tree import (
    DecisionTreeRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

import joblib


# Cargar dataset

dataset = pd.read_csv(
    "../data/processed/dataset_modelado.csv"
)

# Definir variables predictoras

features = [
    "neutral",
    "tournament_weight",
    "fifa_rank_diff",
    "fifa_points_diff",
    "elo_diff",
    "form_points_diff",
    "form_goals_for_diff",
    "form_goals_against_diff",
    "form_goal_balance_diff"
]

# Definir variable objetivo

target = "goal_diff"

X = dataset[features]
y = dataset[target]

# Dividir datos

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Escalar variables

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entrenar Regresión Lineal

lr = LinearRegression()

lr.fit(
    X_train_scaled,
    y_train
)

y_pred_lr = lr.predict(
    X_test_scaled
)

# Evaluar Regresión Lineal

mae_lr = mean_absolute_error(
    y_test,
    y_pred_lr
)

rmse_lr = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_lr
    )
)

r2_lr = r2_score(
    y_test,
    y_pred_lr
)

# Entrenar Random Forest

rf = RandomForestRegressor(
    n_estimators=1000,
    max_depth=5,
    random_state=42,
    n_jobs=-1
)

rf.fit(
    X_train,
    y_train
)

y_pred_rf = rf.predict(X_test)

# Evaluar Random Forest

mae_rf = mean_absolute_error(
    y_test,
    y_pred_rf
)

rmse_rf = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_rf
    )
)

r2_rf = r2_score(
    y_test,
    y_pred_rf
)

# Entrenar XGBoost

xgb = XGBRegressor(
    n_estimators=300,
    learning_rate=0.01,
    max_depth=4,
    random_state=42
)

xgb.fit(
    X_train,
    y_train
)

y_pred_xgb = xgb.predict(X_test)

# Evaluar XGBoost

mae_xgb = mean_absolute_error(
    y_test,
    y_pred_xgb
)

rmse_xgb = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_xgb
    )
)

r2_xgb = r2_score(
    y_test,
    y_pred_xgb
)

# Entrenar KNN

knn = KNeighborsRegressor(
    n_neighbors=5
)

knn.fit(
    X_train_scaled,
    y_train
)

y_pred_knn = knn.predict(
    X_test_scaled
)

# Evaluar KNN

mae_knn = mean_absolute_error(
    y_test,
    y_pred_knn
)

rmse_knn = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_knn
    )
)

r2_knn = r2_score(
    y_test,
    y_pred_knn
)

# Entrenar SVR

svr = SVR(
    kernel="rbf",
    C=1.0,
    epsilon=0.1
)

svr.fit(
    X_train_scaled,
    y_train
)

y_pred_svr = svr.predict(
    X_test_scaled
)

# Evaluar SVR

mae_svr = mean_absolute_error(
    y_test,
    y_pred_svr
)

rmse_svr = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_svr
    )
)

r2_svr = r2_score(
    y_test,
    y_pred_svr
)

# Entrenar Árbol de Decisión

dt = DecisionTreeRegressor(
    random_state=42
)

dt.fit(
    X_train,
    y_train
)

y_pred_dt = dt.predict(
    X_test
)

# Evaluar Árbol de Decisión

mae_dt = mean_absolute_error(
    y_test,
    y_pred_dt
)

rmse_dt = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_dt
    )
)

r2_dt = r2_score(
    y_test,
    y_pred_dt
)

# Entrenar Ridge

ridge = Ridge(
    alpha=1.0
)

ridge.fit(
    X_train_scaled,
    y_train
)

y_pred_ridge = ridge.predict(
    X_test_scaled
)

# Evaluar Ridge

mae_ridge = mean_absolute_error(
    y_test,
    y_pred_ridge
)

rmse_ridge = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_ridge
    )
)

r2_ridge = r2_score(
    y_test,
    y_pred_ridge
)

# Optimizar XGBoost

param_grid = {
    "n_estimators": [100, 300, 500, 700],
    "max_depth": [2, 3, 4, 5, 6],
    "learning_rate": [0.005, 0.01, 0.05, 0.1],
    "subsample": [0.8, 1.0],
    "colsample_bytree": [0.8, 1.0]
}

grid_xgb = GridSearchCV(
    estimator=XGBRegressor(
        random_state=42
    ),
    param_grid=param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

grid_xgb.fit(
    X_train,
    y_train
)

best_xgb = grid_xgb.best_estimator_

pred_xgb_opt = best_xgb.predict(
    X_test
)

mae_xgb_opt = mean_absolute_error(
    y_test,
    pred_xgb_opt
)

rmse_xgb_opt = np.sqrt(
    mean_squared_error(
        y_test,
        pred_xgb_opt
    )
)

r2_xgb_opt = r2_score(
    y_test,
    pred_xgb_opt
)

# Comparar modelos

resultados = pd.DataFrame({
    "Modelo": [
        "Linear Regression",
        "Ridge",
        "SVR",
        "Random Forest",
        "XGBoost",
        "KNN",
        "Decision Tree",
        "XGBoost Optimizado"
    ],
    "MAE": [
        mae_lr,
        mae_ridge,
        mae_svr,
        mae_rf,
        mae_xgb,
        mae_knn,
        mae_dt,
        mae_xgb_opt
    ],
    "RMSE": [
        rmse_lr,
        rmse_ridge,
        rmse_svr,
        rmse_rf,
        rmse_xgb,
        rmse_knn,
        rmse_dt,
        rmse_xgb_opt
    ],
    "R2": [
        r2_lr,
        r2_ridge,
        r2_svr,
        r2_rf,
        r2_xgb,
        r2_knn,
        r2_dt,
        r2_xgb_opt
    ]
})

resultados = resultados.sort_values(
    by="R2",
    ascending=False
)

# Guardar resultados

resultados.to_csv(
    "comparacion_modelos.csv",
    index=False
)

# Guardar modelos

joblib.dump(
    scaler,
    "scaler.pkl"
)

joblib.dump(
    lr,
    "modelo_regresion_lineal.pkl"
)

joblib.dump(
    ridge,
    "modelo_ridge.pkl"
)

joblib.dump(
    rf,
    "modelo_random_forest.pkl"
)

joblib.dump(
    xgb,
    "modelo_xgboost.pkl"
)

joblib.dump(
    best_xgb,
    "modelo_xgboost_optimizado.pkl"
)

print(resultados)