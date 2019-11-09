from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
db = SQLAlchemy(app)

#Criando o Banco de Dados
class CadastroDB(db.Model):

    __tablename__ = 'Cadastros'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String, nullable = False)
    endereco = db.Column(db.String, nullable = False)
    telefone = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

    def __init__(self, nome, endereco, telefone, email):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

db.create_all()

#Página HOME =========================================================
@app.route('/') 
def index():
    return render_template('index.html')


@app.route('/cadastro')
def cadastrar_cliente(): 
    return render_template('cadastro.html') #redireciona para página cadastro

@app.route('/lista')
def lista_clientes():
    tabela = CadastroDB.query.order_by(CadastroDB.id).all()
    return render_template('lista_clientes.html', tabela=tabela)

@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

#Página CADASTRO===========================================================
@app.route('/cadastro', methods = ['POST', 'GET'])
def inserirDados():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        #Dando uma funcionalidade para o botão "cadastrar"
        #Verifico se todos os dados já foram preenchidos
        if nome and endereco and telefone and email:
            dadosGravados = CadastroDB(nome, endereco, telefone, email)
            #Salvo os dados inseridos dentro do Banco de Dados
            try:
                db.session.add(dadosGravados)
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return "Erro ao gravar os dados!"
#Página LISTA======================================================
@app.route('/excluir/<int:id>')
def excluir(id):

    cliente = CadastroDB.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        tabela = CadastroDB.query.all()
        return render_template('lista_clientes.html', tabela=tabela)
    except:
        return "Erro ao deletar cliente!"


@app.route('/atualizar/<int:id>', methods = ['POST', 'GET'])
def atualizar(id):

    cliente = CadastroDB.query.get_or_404(id)
    try:
        if request.method == 'POST':
            nome = request.form.get('nome')
            endereco = request.form.get('endereco')
            telefone = request.form.get('telefone')
            email = request.form.get('email')

        
            if nome and endereco and telefone and email:
                cliente.nome = nome
                cliente.endereco = endereco
                cliente.telefone = telefone
                cliente.email = email

                db.session.commit()

                return redirect(url_for('lista_clientes'))

        return render_template('atualizar.html', cliente = cliente)

    except:
        return "Erro ao atualizar dados do cliente!"



#Página Pesquisa=================================================================
@app.route('/pesquisa', methods = ['POST', 'GET'])
def pesquisar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        #print(id)
        if nome:
            tabela = CadastroDB.query.filter_by(nome = nome)
            return render_template('pesquisa.html', tabela=tabela)
        else:
            return "Digite um nome!"


if __name__ == "__main__":
    app.run(debug=True)