from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import datetime
import os
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)
DB_path = "database/registros.db"
EXVEL_path = "exports/registros.xlsx"


os.makedirs('database', exist_ok=True)
os.makedirs('exports', exist_ok=True)
os.makedirs('static/signatures', exist_ok=True)

def init_db():
    with sqlite3.connect(DB_path) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            nome TEXT,
            numero_tiquete TEXT,
            peso_bruto REAL,
            peso_liquido REAL,
            destino TEXT,
            assinatura_path TEXT
        )
                     
    ''')
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sadjskdlslda
