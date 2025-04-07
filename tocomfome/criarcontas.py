from flask import render_template, url_for, request, redirect, flash
from tocomfome import app, database, bcrypt
from tocomfome.models import Prato, Sobremesa, Bebida, Cliente, Funcionario, Usuario

with app.app_context():
    senha_cript = bcrypt.generate_password_hash('admin123')
    funcionario = Funcionario(nome='admin', email='admin@gmail.com', senha=senha_cript)
    database.session.add(funcionario)
    database.session.commit()