from Jogos import Jogo
from Usuario import Usuario
from flask import Flask, render_template, request, redirect, session, flash, \
    url_for

app = Flask(__name__)
app.secret_key = 'random'

usuario1 = Usuario('bia', 'Bianca', 'Thunder')
usuario2 = Usuario('joao', 'João', 'Trovao')
usuario3 = Usuario('ana', 'Ana', '123456')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2, 
            usuario3.id: usuario3}


jogo1 = Jogo('Tetris', 'Puzzle', 'Polystation')
jogo2 = Jogo('A.C.: Brotherhood', 'Ação/Aventura', 'PS3')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS4')
lista = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/insere-jogo')
def insere_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('insere_jogo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Erro de login ou senha. Tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
