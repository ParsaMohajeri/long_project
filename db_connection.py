import mysql.connector

# set up a database connection
try:
    connecting=mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="proffesional"
    )
    Activator=connecting.cursor()
    print("Database connection successful")
except:
    print("Error connecting to database")
