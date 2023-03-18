import sqlite3

# Connect to the database
  
def dbconfig():
  try:
    # Connect to the database
    conn = sqlite3.connect('manager.db')
    # Create a cursor object to execute SQL queries
    # print('Connected successfully ', conn)
    # printc("[green][+][/green] Connected to db")
  except Exception as e:
    print("[red][!] An error occurred while trying to connect to the database[/red]")
  return conn

