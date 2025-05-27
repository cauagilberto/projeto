from flask import Flask, render_template, request, send_file
import sqlite3
import pandas as pd
import datetime
import os
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
from PIL import Image
import io
import sys

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
            data TEXT,
            time TEXT,        
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
        nome = request.form['nome']
        numero_tiquete = request.form['numero_tiquete']
        peso_bruto = float(request.form['peso_bruto'])
        peso_liquido = float(request.form['peso_liquido'])
        destino = request.form['destino']
        data = request.form['data']
        time = datetime.datetime.now().strftime("%H:%M:%S")

        assinatura = request.form['assinatura']
        timestamp = datetime.datetime.now().timestamp()
        assinatura_path = f'static/signatures/{timestamp}.png'

        with open(assinatura_path, 'wb') as fh:
            import base64
            fh.write(base64.b64decode(assinatura.split(',')[1]))

        with sqlite3.connect(DB_path) as conn:
            conn.execute('''
            INSERT INTO registros (data, time, nome, numero_tiquete, peso_bruto, peso_liquido, destino, assinatura_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data, time, nome, numero_tiquete, peso_bruto, peso_liquido, destino, assinatura_path))

        #export to Excel
        df = pd.read_sql_query("SELECT * FROM registros", sqlite3.connect(DB_path))
        df.to_excel(EXVEL_path, index=False)

        #gerar PDF
        pdf_path = f'exports/registro_{timestamp}.pdf'
        c = canvas.Canvas(pdf_path)
        c.drawString(50, 800, f"Data: {data}")
        c.drawString(50, 780, f"Hora: {time}")
        c.drawString(50, 760, f"Nome: {nome}")
        c.drawString(50, 740, f"Número do Tiquete: {numero_tiquete}")
        c.drawString(50, 720, f"Peso Bruto: {peso_bruto} kg")
        c.drawString(50, 700, f"Peso Líquido: {peso_liquido} kg")
        c.drawString(50, 680, f"Destino: {destino}")
        c.drawImage(assinatura_path, 50, 600, width=200, height=100)
        c.save()

        return {"status": "success"}
    
    #mostrar registros
    with sqlite3.connect(DB_path) as conn:
        registros = conn.execute("SELECT *FROM registros ORDER BY id DESC LIMIT 10").fetchall()

    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    import os
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)