from tocomfome import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_usuario(user_id):
    # Carrega o usuário diretamente da tabela base 'Usuario'
    return Usuario.query.get(int(user_id))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    tipo = database.Column(database.String, nullable=False)  # 'cliente' ou 'funcionario'

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'usuario'
    }

    def get_id(self):
        return str(self.id)  # Retorna o ID como string para Flask-Login

class Cliente(Usuario):
    __mapper_args__ = {
        'polymorphic_identity': 'cliente'
    }

class Funcionario(Usuario):
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario'
    }




class Prato(database.Model):
    id_prato = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    ingrediente = database.Column(database.String, nullable=False)


class Sobremesa(database.Model):
    id_sobremesa = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    ingrediente = database.Column(database.String, nullable=False)


class Bebida(database.Model):
    id_bebida = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    preco = database.Column(database.Float, nullable=False)
    teor_alcoolico = database.Column(database.Float, nullable=False)

class Pedido(database.Model):
    id_pedido = database.Column(database.Integer, primary_key=True, autoincrement=True)
    codigo_pedido = database.Column(database.String, nullable=False) 
    id_item = database.Column(database.Integer, nullable=False)
    nome_item = database.Column(database.String, nullable=False)
    quantidade_item = database.Column(database.Integer, nullable=False)
    preco_item = database.Column(database.Float, nullable=False)
    valor_total = database.Column(database.Float, nullable=False)
    id_usuario_pedido = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    status = database.Column(database.String, nullable=False, default='preparando')


    usuario = database.relationship('Usuario', backref='pedidos')





