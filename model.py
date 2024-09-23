import duckdb
from pandas import get_dummies
from sklearn.linear_model import LinearRegression

from pins import board_folder
from vetiver import VetiverModel, vetiver_pin_write


# Get Data
con = duckdb.connect('my-db.duckdb')
df = con.execute('SELECT * FROM penguins').fetchdf().dropna()
con.close()


# Define Model and Fit
X = get_dummies(df[["bill_length_mm", "species", "sex"]], drop_first=True)
y = df["body_mass_g"]

model = LinearRegression().fit(X, y)


# Turn into Vetiver Model
v = VetiverModel(model, model_name='penguin_model', prototype_data=X)

# Save to Board
model_board = board_folder(
    "./data/model",
    allow_pickle_read=True
)

vetiver_pin_write(model_board, v)
