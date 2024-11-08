from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            imc REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Rota para a página de cálculo do IMC
@app.route("/", methods=["GET", "POST"])
def calcular_imc():
    if request.method == "POST":
        nome = request.form["nome"]
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        
        # Cálculo do IMC
        imc = peso / (altura ** 2)
        if imc < 18.5:
            status = "Abaixo do peso"
        elif 18.5 <= imc <= 24.9:
            status = "Peso normal"
        else:
            status = "Acima do peso"
        
        # Inserindo os dados no banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pessoas (nome, peso, altura, imc, status) VALUES (?, ?, ?, ?, ?)', 
                       (nome, peso, altura, imc, status))
        conn.commit()
        conn.close()
        
        return redirect(url_for("ver_dados"))
    return render_template("index.html")

# Rota para exibir os dados armazenados
@app.route("/dados")
def ver_dados():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pessoas')
    dados = cursor.fetchall()
    conn.close()
    return render_template("dados.html", dados=dados)

if __name__ == "_main_":
    app.run(debug=True)