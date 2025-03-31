import pyodbc
import pandas as pd

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.0.207,1433;"
    "DATABASE=AdventureWorks2022;"
    "UID=cezar;PWD=Verte#123;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM Person.Person')
rows = cursor.fetchall()
columns = [column[0] for column in cursor.description]
df = pd.DataFrame.from_records(rows, columns=columns)
print(df)
