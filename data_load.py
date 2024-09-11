import duckdb
from palmerpenguins import load_penguins

con = duckdb.connect('my-db.duckdb')
df = load_penguins()
con.execute('CREATE TABLE penguins AS SELECT * FROM df')
con.close()
