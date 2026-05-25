import os
import time
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Permite que o Frontend acesse a API

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'meudb')
DB_USER = os.environ.get('POSTGRES_USER', 'usuario')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'senha')

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("Não foi possível conectar ao banco de dados.")

# Cria a tabela se não existir ao iniciar a API
try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS acessos (
            id SERIAL PRIMARY KEY, 
            tipo VARCHAR(50) NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print(f"Erro ao inicializar banco: {e}")

@app.route('/pontos', methods=['GET'])
def listar_pontos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, tipo, data_hora FROM acessos ORDER BY data_hora DESC;')
    registros = cur.fetchall()
    cur.close()
    conn.close()
    
    pontos = []
    for reg in registros:
        pontos.append({"id": reg[0], "tipo": reg[1], "data_hora": reg[2]})
    return jsonify(pontos)

@app.route('/pontos', methods=['POST'])
def bater_ponto():
    dados = request.get_json()
    tipo = dados.get('tipo', 'Desconhecido')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO acessos (tipo) VALUES (%s);', (tipo,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"mensagem": "Ponto registrado com sucesso!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)