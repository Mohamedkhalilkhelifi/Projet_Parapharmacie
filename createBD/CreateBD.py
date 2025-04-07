import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    port='3300',
)

mycursor = mydb.cursor()

# Création de la base de données si elle n'existe pas
mycursor.execute("CREATE DATABASE IF NOT EXISTS parapharmacie")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)
