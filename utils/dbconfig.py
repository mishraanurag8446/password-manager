import hashlib
import os
import pyperclip
from aesutil import encrypt, decrypt
import sqlite3
import string
from random import choices
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

db_name = 'manager.db'
userAuth_tb = 'secrets'
userEntry_tb = 'entries'


# Connect to the database
def dbconfig():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
    except Exception as e:
        print(e)
    return conn


def checkConfig():
    conn = dbconfig()
    c = conn.cursor()
    # Execute a SQL query to check if the table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (userAuth_tb,))
    row = c.fetchone()
    c.close()
    conn.close()
    if row is not None:
        return True
    return False


def generateDeviceSecret(length=12):
    return ''.join(choices(string.ascii_uppercase + string.digits, k=length))


def make():
    conn, c = None, None
    if checkConfig():
        return
    try:
        # Create database
        conn = dbconfig()
        c = conn.cursor()
        c.execute(
            f'''CREATE TABLE IF NOT EXISTS {userAuth_tb}(masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)''')
        c.execute(
            f'''CREATE TABLE IF NOT EXISTS {userEntry_tb}(sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, 
            username TEXT, password TEXT NOT NULL)''')
        conn.commit()

    except Exception as e:
        print(e)
    finally:
        c.close()
        conn.close()


def registerDevice(mp):
    if mp == "":
        return False
    try:
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
        # Generate a device secret
        ds = generateDeviceSecret()
        # Add them to db
        conn = dbconfig()
        c = conn.cursor()
        c.execute(f"INSERT INTO {userAuth_tb}(masterkey_hash, device_secret) values (?, ?)", (hashed_mp, ds))
        conn.commit()
        return True
    except Exception as e:
        print(e)
    finally:
        c.close()
        conn.close()
    return False


def delete():
    if not checkConfig():
        return
    os.remove(db_name)


def remake():
    delete()
    make()


def validateMasterPassword(mp):
    result = None
    try:
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
        conn = dbconfig()
        c = conn.cursor()
        query = f"SELECT * FROM {userAuth_tb}"
        c.execute(query)
        result = c.fetchone()
    except Exception as e:
        print(e)
    if result and hashed_mp != result[0]:
        return False
    return True


def computeMasterKey():
    conn = dbconfig()
    c = conn.cursor()
    query = f"SELECT * FROM {userAuth_tb}"
    c.execute(query)
    result = c.fetchone()
    password = result[0]
    salt = result[1]
    # print(password, salt)
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def checkEntry(sitename=None, siteurl=None):
    query = ""
    # print(sitename, siteurl)
    if sitename != '':
        query = f"SELECT * FROM {userEntry_tb} WHERE sitename = '{sitename}'"
    elif siteurl != '':
        query = f"SELECT * FROM {userEntry_tb} WHERE siteurl = '{siteurl}'"
    db = dbconfig()
    cursor = db.cursor()
    # query = f"SELECT * FROM {userEntry_tb} WHERE sitename = '{sitename}' OR siteurl = '{siteurl}' OR email = '{email}' OR username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchone()

    if results is not None and len(results) != 0 :
        return True
    return False


def addEntry(sitename, siteurl, email, username, password):
    mk = computeMasterKey()
    encrypted = encrypt(key=mk, source=password, keyType="bytes")
    # Check if the entry already exists
    if checkEntry(sitename, siteurl):
        try:
            conn = dbconfig()
            c = conn.cursor()
            query = f"UPDATE {userEntry_tb} SET password='{encrypted}' where sitename = '{sitename}' OR siteurl = '{siteurl}'"
            c.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            c.close()
            conn.close()
        return 1
    try:
        conn = dbconfig()
        c = conn.cursor()
        query = f"INSERT INTO  {userEntry_tb}(sitename, siteurl, email, username, password) values (?,?,?,?,?)"
        c.execute(query, (sitename, siteurl, email, username, encrypted))
        conn.commit()
    except Exception as e:
        print(e)
        return 0
    finally:
        c.close()
        conn.close()
    return 1


def retrieveEntries(sitename, siteurl):
    query = ""
    # print(sitename, siteurl)
    if sitename != '':
        query = f"SELECT * FROM {userEntry_tb} WHERE sitename = '{sitename}'"
    elif siteurl != '':
        query = f"SELECT * FROM {userEntry_tb} WHERE siteurl = '{siteurl}'"
    try:
        conn = dbconfig()
        c = conn.cursor()
        c.execute(query)
        results = c.fetchone()
        print(results)
        mk = computeMasterKey()
        # print(results[4])
        if results is not None:
            decrypted = decrypt(key=mk, source=results[4], keyType="bytes")
            pyperclip.copy(decrypted.decode())
            if pyperclip.paste() == decrypted.decode():
                return True
            else:
                return False
    except Exception as e:
        print(e)
    finally:
        c.close()
        conn.close()
    return False


if __name__ == "__main__":
    pass
    # remake()
    # print(registerDevice('1234567890'))
    # print(validateMasterPassword('1234567890'))
    # print(addEntry('facebook', 'fb.com', 'abc@gmail.com', 'abc', '12345'))

    # print(computeMasterKey())
    print(retrieveEntries(sitename='facebook',siteurl=''))
