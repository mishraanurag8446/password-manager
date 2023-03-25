from dbconfig import dbconfig, computeMasterKey, userEntry_tb
from aesutil import decrypt, encrypt
import pyperclip


def retrieveEntries(sitename=None, siteurl=None):
    try:
        conn = dbconfig()
        c = conn.cursor()
        query = f"SELECT * FROM {userEntry_tb} WHERE sitename = '{sitename}' OR siteurl = '{siteurl}'"
        c.execute(query)
        results = c.fetchone()
        print(results)
        mk = computeMasterKey()
        print(results[4])
        decrypted = decrypt(key=mk, source=results[4], keyType="bytes")
        pyperclip.copy(decrypted.decode())
    except Exception as e:
        print(e)
    finally:
        c.close()
        conn.close()


if __name__ == '__main__':
    mk = computeMasterKey()
    encrypted = encrypt(key=mk, source='hello', keyType="bytes")
    # print(decrypt(mk, '8ZR7YhotfX0xrAk3YZ2KQUV0U7WcXuTN9v1nwYm/Eus=', keyType="bytes").decode())
    retrieveEntries(siteurl='fb.com')
