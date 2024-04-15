from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'slaptas_raktas'

# Sukuriamas prisijungimas prie SQLite duomenų bazės
conn = sqlite3.connect('uzduociu_db.db', check_same_thread=False)
c = conn.cursor()

# Sukuriama duomenų bazė ir lentelė, jei jos dar neegzistuoja
c.execute('''CREATE TABLE IF NOT EXISTS užduotys
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             pavadinimas TEXT NOT NULL,
             apibūdinimas TEXT NOT NULL,
             statusas TEXT NOT NULL,
             vartotojas TEXT NOT NULL)''')
conn.commit()

@app.route('/')
def index():
    c.execute("SELECT * FROM užduotys")
    tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/prideti', methods=['POST'])
def prideti_uzduoti():
    if request.method == 'POST':
        naujas_pavadinimas = request.form['pavadinimas']
        naujas_apibudinimas = request.form['apibudinimas']
        naujas_statusas = request.form['statusas']
        naujas_vartotojas = request.form['vartotojas']

        c.execute("INSERT INTO užduotys (pavadinimas, apibūdinimas, statusas, vartotojas) VALUES (?, ?, ?, ?)",
                  (naujas_pavadinimas, naujas_apibudinimas, naujas_statusas, naujas_vartotojas))
        conn.commit()

        return redirect(url_for('index'))

@app.route('/redaguoti/<int:uzduoties_id>', methods=['GET', 'POST'])
def redaguoti_uzduoti(uzduoties_id):
    c.execute("SELECT * FROM užduotys WHERE id=?", (uzduoties_id,))
    užduotis = c.fetchone()
    if request.method == 'POST':
        redaguotas_pavadinimas = request.form['pavadinimas']
        redaguotas_apibudinimas = request.form['apibudinimas']
        redaguotas_statusas = request.form['statusas']
        redaguotas_vartotojas = request.form['vartotojas']

        c.execute("UPDATE užduotys SET pavadinimas=?, apibūdinimas=?, statusas=?, vartotojas=? WHERE id=?",
                  (redaguotas_pavadinimas, redaguotas_apibudinimas, redaguotas_statusas, redaguotas_vartotojas, uzduoties_id))
        conn.commit()

        return redirect(url_for('index'))
    return render_template('redaguoti.html', užduotis=užduotis)

@app.route('/istrinti/<int:uzduoties_id>', methods=['POST'])
def istrinti_uzduoti(uzduoties_id):
    c.execute("DELETE FROM užduotys WHERE id=?", (uzduoties_id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/filtruoti', methods=['GET', 'POST'])
def filtruoti_uzduotis():
    if request.method == 'POST':
        statusas = request.form['statusas']
        vartotojas = request.form['vartotojas']
        if statusas == 'Visi' and vartotojas == 'Visi':
            c.execute("SELECT * FROM užduotys")
        elif statusas == 'Visi':
            c.execute("SELECT * FROM užduotys WHERE vartotojas=?", (vartotojas,))
        elif vartotojas == 'Visi':
            c.execute("SELECT * FROM užduotys WHERE statusas=?", (statusas,))
        else:
            c.execute("SELECT * FROM užduotys WHERE statusas=? AND vartotojas=?", (statusas, vartotojas))
        tasks = c.fetchall()
        return render_template('index.html', tasks=tasks)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
