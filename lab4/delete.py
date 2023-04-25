from flask import Flask, render_template, request, redirect, url_for
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("DELETE FROM users")
conn.commit()
conn.close()
