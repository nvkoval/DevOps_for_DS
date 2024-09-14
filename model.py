import duckdb
from pandas import get_dummies
from sklearn.linear_model import LinearRegression

from vetiver import VetiverModel
from pins import board_folder
from vetiver import vetiver_pin_write
from vetiver import VetiverAPI

# Get Data
con = duckdb.connect('my-db.duckdb')
df = con.execute('SELECT * FROM penguins').fetchdf().dropna()
con.close()

df.head(3)


# Define Model and Fit
X = get_dummies(df[["bill_length_mm", "species", "sex"]], drop_first=True)
y = df["body_mass_g"]

model = LinearRegression().fit(X, y)

# Get some information
print(f"R^2 {model.score(X, y):.4f}")
print(f"Intercept {model.intercept_:.4f}")
print(f"Columns {X.columns}")
print(f"Coefficients {model.coef_}")

# Turn into Vetiver Model
v = VetiverModel(model, model_name='penguin_model', prototype_data=X)


# Save to Board
model_board = board_folder(
    "/data/model",
    allow_pickle_read=True
)

vetiver_pin_write(model_board, v)

# Turn model into API
v_api = VetiverAPI(v, check_prototype=True)
# v_api.run(port=8080)
