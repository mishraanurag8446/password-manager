import os
import sys
import string
import random
import hashlib
import sys
from getpass import getpass

from dbconfig import dbconfig
table_name = 'manager.db'

def checkConfig():
	conn = dbconfig()
	c = conn.cursor()
	# Execute a SQL query to check if the table exists
	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
	row = c.fetchone()
	c.close()
	conn.close()
	if row is not None:
		return True
	return False 


def generateDeviceSecret(length=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))


def make():
	if checkConfig():
		return
	try:
		# Create database
		conn = dbconfig()
		c = conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS secrets(masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)''')
		c.execute('''CREATE TABLE IF NOT EXISTS entries(sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)''')
	except Exception as e:
		print(e)


def registerDevice(mp):
	if mp=="":
		return
	# Hash the MASTER PASSWORD
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
	# Generate a device secret
	ds = generateDeviceSecret()
	# Add them to db
	# query = "INSERT INTO secrets (masterkey_hash, device_secret) values (?, ?)",(hashed_mp, ds)
	conn = dbconfig()
	c = conn.cursor()
	c.execute("INSERT INTO secrets (masterkey_hash, device_secret) values (?, ?)",(hashed_mp, ds))
	conn.commit()
	c.close()
	conn.close()

def delete():
	if not checkConfig():
		return
	os.remove(table_name)
	

def remake():
	delete()
	make()


if __name__ == "__main__":
	remake()
	registerDevice('Hellouihio')