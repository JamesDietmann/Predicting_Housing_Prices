#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
#%%
def load_data(filepath):
    """Load the housing dataset."""
    df = pd.read_csv(filepath)
    return df
#%%
housing = load_data("house-prices-advanced-regression-techniques/train.csv")

X = housing[[
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "TotalBsmtSF",
    "FullBath",
    "YearBuilt"
]]
y = housing["SalePrice"]
#%%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
#%%
lr_model = LinearRegression()
dt_model = DecisionTreeRegressor(random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

for model in [lr_model, dt_model, rf_model]:
    model.fit(X_train, y_train)
#%%
models = {
    "Linear Regression": lr_model,
    "Decision Tree":     dt_model,
    "Random Forest":     rf_model,
}

for name, model in models.items():
    preds = model.predict(X_test)
    r2    = model.score(X_test, y_test)
    rmse  = np.sqrt(mean_squared_error(y_test, preds))
    mae   = mean_absolute_error(y_test, preds)
    print(f"{name:20s}  R²={r2:.4f}  RMSE=${rmse:,.0f}  MAE=${mae:,.0f}")
#%%
for name, model in models.items():
    train_r2 = model.score(X_train, y_train)
    test_r2  = model.score(X_test, y_test)
    print(f"{name:20s}  Train R²={train_r2:.4f}  Test R²={test_r2:.4f}")
#%%
for name, model in models.items():
    preds = model.predict(X_test)
    
    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, preds, alpha=0.4)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Actual Price")
    plt.ylabel("Predicted Price")
    plt.title(name)
    plt.tight_layout()
    plt.show()
#%%
feat_imp = pd.Series(rf_model.feature_importances_, index=X.columns)
feat_imp.sort_values().plot(kind="barh")
plt.title("Feature Importances — Random Forest")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()
# %%
