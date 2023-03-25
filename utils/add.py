from dbconfig import dbconfig, userEntry_tb, computeMasterKey
import aesutil


def checkEntry(sitename=None, siteurl=None, email=None, username=None):
    db = dbconfig()
    cursor = db.cursor()
    query = f"SELECT * FROM {userEntry_tb} WHERE sitename = '{sitename}' OR siteurl = '{siteurl}' OR email = '{email}' OR username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) != 0:
        return True
    return False


def addEntry(sitename, siteurl, email, username, password):

    mk = computeMasterKey()
    encrypted = aesutil.encrypt(key=mk, source=password, keyType="bytes")
    # Check if the entry already exists
    if checkEntry(sitename, siteurl, email, username):
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


if __name__ == '__main__':
    addEntry('facebook', 'fb.com', 'abc@gmail.com', 'abc', '12345')
