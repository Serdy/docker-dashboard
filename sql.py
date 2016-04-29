from flask import g
import sqlite3


def NAME():
    email_addresses = g.db.execute("SELECT NAME FROM test;").fetchall()
    return email_addresses
    
