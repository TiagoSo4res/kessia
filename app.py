from flask import Flask, render_template, request, jsonify, session
import random
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'  # Altere para uma chave segura em produção

# Arquivo para armazenar os participantes
ARQUIVO_PARTICIPANTES = 'participantes.txt'
ARQUIVO_SORTEIO = 'sorteios.json'

def carregar_participantes():
    if os.path.exists(ARQUIVO_PARTICIPANTES):
        with open(ARQUIVO_PARTICIPANTES, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]
    return []

def salvar_participantes(participantes):
    with open(ARQUIVO_PARTICIPANTES, 'w', encoding='utf-8') as f:
        for participante in participantes:
            f.write(participante + '\n')

def carregar_sorteios():
    if os.path.exists(ARQUIVO_SORTEIO):
        with open(ARQUIVO_SORTEIO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_sorteio(nome, amigo_secreto):
    sorteios = carregar_sorteios()
    sorteios[nome] = amigo_secreto
    with open(ARQUIVO_SORTEIO, 'w', encoding='utf-8') as f:
        json.dump(sorteios, f)

@app.route('/')
def index():
    participantes = carregar_participantes()
    return render_template('index.html', participantes=participantes)

@app.route('/adicionar', methods=['POST'])
def adicionar_participante():
    nome = request.form.get('nome', '').strip()
    if nome:
        participantes = carregar_participantes()
        if nome not in participantes:
            participantes.append(nome)
            salvar_participantes(participantes)
    return jsonify({'sucesso': True, 'participantes': participantes})

@app.route('/remover', methods=['POST'])
def remover_participante():
    nome = request.form.get('nome', '').strip()
    if nome:
        participantes = carregar_participantes()
        if nome in participantes:
            participantes.remove(nome)
            salvar_participantes(participantes)
    return jsonify({'sucesso': True, 'participantes': participantes})

@app.route('/sortear', methods=['POST'])
def sortear():
    participantes = carregar_participantes()
    
    if len(participantes) < 2:
        return jsonify({'erro': 'São necessários pelo menos 2 participantes'})
    
    # Embaralha os participantes
    embaralhados = participantes.copy()
    random.shuffle(embaralhados)
    
    # Cria pares garantindo que ninguém tire a si mesmo
    pares = {}
    tentativas = 0
    max_tentativas = 100
    
    while tentativas < max_tentativas:
        embaralhados = participantes.copy()
        random.shuffle(embaralhados)
        valido = True
        
        for i in range(len(participantes)):
            if participantes[i] == embaralhados[i]:
                valido = False
                break
        
        if valido:
            for i in range(len(participantes)):
                pares[participantes[i]] = embaralhados[i]
            break
        
        tentativas += 1
    
    if tentativas == max_tentativas:
        # Se não conseguir após muitas tentativas, usa método alternativo
        for i in range(len(participantes)):
            pares[participantes[i]] = embaralhados[(i + 1) % len(participantes)]
    
    # Salva o sorteio
    for nome, amigo in pares.items():
        salvar_sorteio(nome, amigo)
    
    return jsonify({'sucesso': True, 'pares': pares})

@app.route('/consultar', methods=['POST'])
def consultar():
    nome = request.form.get('nome', '').strip()
    if nome:
        sorteios = carregar_sorteios()
        amigo_secreto = sorteios.get(nome)
        if amigo_secreto:
            return jsonify({'sucesso': True, 'amigo_secreto': amigo_secreto})
        else:
            return jsonify({'erro': 'Nome não encontrado no sorteio'})
    return jsonify({'erro': 'Nome não informado'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)