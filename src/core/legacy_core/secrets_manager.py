import os
import sqlite3
from base64 import b64decode, b64encode

# A simple XOR wrapper for MVP 'encryption'. In a real scenario, use cryptography.fernet
SECRET_KEY = b"ReconX_Secret_Key_12345!"


def xor_crypt(text, encode=False):
    key = SECRET_KEY
    if encode:
        text = text.encode()
    res = bytearray()
    for i, c in enumerate(text):
        res.append(c ^ key[i % len(key)])
    if encode:
        return b64encode(res).decode()
    return res.decode()


class SecretsManager:
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "secrets.db"))

    @classmethod
    def _init_db(cls):
        if not os.path.exists("workspace"):
            os.makedirs("workspace")
        conn = sqlite3.connect(cls.DB_PATH)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS secrets
                     (id TEXT PRIMARY KEY, value TEXT)""")
        conn.commit()
        return conn

    @classmethod
    def set_secret(cls, key, value):
        conn = cls._init_db()
        c = conn.cursor()
        enc_val = xor_crypt(value, encode=True)
        c.execute("REPLACE INTO secrets (id, value) VALUES (?, ?)", (key, enc_val))
        conn.commit()
        conn.close()

    @classmethod
    def get_secret(cls, key):
        conn = cls._init_db()
        c = conn.cursor()
        c.execute("SELECT value FROM secrets WHERE id=?", (key,))
        row = c.fetchone()
        conn.close()
        if row:
            try:
                dec = b64decode(row[0])
                return xor_crypt(dec, encode=False)
            except:
                return None
        return None
