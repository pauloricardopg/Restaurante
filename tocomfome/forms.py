from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from tocomfome.models import Cliente, Funcionario


class FormCriarConta(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

    def validate_email(self, email):
        cliente = Cliente.query.filter_by(email=email.data).first()
        if cliente:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email')
        

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')
    


class FormPrato(FlaskForm):
    nome_prato = StringField('Nome do Prato', validators=[DataRequired(), Length(min=2, max=50)])
    preco_prato = DecimalField('Preço (R$)', validators=[DataRequired(), NumberRange(min=0)], places=2)
    ingredientes_prato = TextAreaField('Ingredientes', validators=[DataRequired(), Length(min=5, max=500)])
    botao_submit_prato = SubmitField('Salvar')
    


class FormSobremesa(FlaskForm):
    nome_sobremesa = StringField('Nome da Sobremesa', validators=[DataRequired(), Length(min=2, max=50)])
    preco_sobremesa = DecimalField('Preço (R$)', validators=[DataRequired(), NumberRange(min=0)], places=2)
    ingredientes_sobremesa = TextAreaField('Ingredientes', validators=[DataRequired(), Length(min=5, max=500)])
    botao_submit_sobremesa = SubmitField('Salvar')
    

class FormBebida(FlaskForm):
    nome_bebida = StringField('Nome da Bebida', validators=[DataRequired(), Length(min=2, max=50)])
    preco_bebida = DecimalField('Preço (R$)', validators=[DataRequired(), NumberRange(min=0)], places=2)
    teor_alcoolico = DecimalField('Teor alcoolico da bebida', validators=[DataRequired(), NumberRange(min=0)], places=2)
    botao_submit_bebida= SubmitField('Salvar')
    
class FormQuantidade(FlaskForm):
    item_id = HiddenField('ID do item', validators=[DataRequired()])
    quantidade_prato = IntegerField('Quantidade')  # Sem DataRequired
    quantidade_sobremesa = IntegerField('Quantidade')
    quantidade_bebida = IntegerField('Quantidade')
    botao_submit = SubmitField('Salvar')


class FormExcluir(FlaskForm):
    nome = StringField('Nome do item que vai ser excluido', validators=[DataRequired(), Length(min=2, max=50)])
    botao_submit_excluir= SubmitField('Salvar')

