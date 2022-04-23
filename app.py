
from flask import Flask, flash, render_template,request,redirect,session,url_for
from urllib.request import urlopen, urlretrieve
import requests
from bs4 import BeautifulSoup
# class jogo:
#     def __init__(self, nome, categoria, console):
#         self.nome = nome
#         self.categoria = categoria
#         self.console = console


# jogo01 = jogo('tetris', 'puzzle', 'atari')
# jogo02 = jogo('mario', 'aventura', 'super nintendo')
# jogo03 = jogo('sonic', 'aventura', 'mega drive')
# jogos = [jogo01,jogo02,jogo03]

pergunta = []

class passei_direto:
    def __init__(self, url):
        self.url = url
        url_requisicao = url
        headers = {'User-Agent': 'Mozilla/5.0','content-type': 'application/x-www-form-urlencoded'}

        try:
            requisicao = requests.get(url, headers=headers)
            resposta = BeautifulSoup(requisicao.text, 'html.parser')
            questoes = resposta.find('pre').get_text().split("Pergunta")

            for questao in questoes:
                pergunta.append(questao)
        except:
            flash('Verifique se a url é do Passei direto')
            pergunta.append('Ops, algo deu errado... Tente novamente')


        

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario não logado')
        return redirect(url_for('login'))
    return render_template('lista.html', titulo = 'Sua prova', pergunta = pergunta)

@app.route('/passeiDireto')
def novo():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Usuario não logado')
        return redirect(url_for('login'))

    return render_template('novo.html', titulo = 'APP-Resposta')

@app.route('/criar', methods = ['POST'])
def criar():

    # nome = request.form['nome']
    # categoria = request.form['categoria']
    # console = request.form['console']

    url = request.form['url']

    resposta = passei_direto(url)

    #pergunta.append(resposta)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    #proxima = request.args.get('proxima')
    return render_template('login.html')

@app.route('/autenticar', methods = ['POST'])
def autenticar():
    if 'jordan' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash('Logado com sucesos!')
        return redirect('/passeiDireto')
    else:
        flash('senha ou usuario não confere!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efeteuda com suceso')

    return redirect(url_for('login'))

app.run( )
