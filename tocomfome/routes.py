from flask import render_template, url_for, request, redirect, flash, session
from tocomfome import app, database, bcrypt
from tocomfome.forms import FormPrato, FormBebida, FormSobremesa, FormQuantidade, FormExcluir, FormLogin, FormCriarConta
from tocomfome.models import Prato, Sobremesa, Bebida, Usuario, Cliente, Funcionario, Pedido
from flask_login import login_user, logout_user, login_required, current_user
import uuid
from tocomfome.models import Pedido

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form_quantidade = FormQuantidade()

    pratos = Prato.query.all()
    sobremesas = Sobremesa.query.all()
    bebidas = Bebida.query.all()

    carrinho_key = f'carrinho_{current_user.id}'
    carrinho = session.get(carrinho_key, [])

    if form_quantidade.validate_on_submit() and 'botao_submit' in request.form:
        item_id = int(form_quantidade.item_id.data)
        tipo_item = request.form.get('tipo_item')

        item = None
        quantidade = 0

        if tipo_item == "prato":
            item = Prato.query.get(item_id)
            quantidade = form_quantidade.quantidade_prato.data
        elif tipo_item == "sobremesa":
            item = Sobremesa.query.get(item_id)
            quantidade = form_quantidade.quantidade_sobremesa.data
        elif tipo_item == "bebida":
            item = Bebida.query.get(item_id)
            quantidade = form_quantidade.quantidade_bebida.data

        if quantidade > 0 and item:
            carrinho.append({
                'id': str(uuid.uuid4()),
                'tipo': tipo_item,
                'item_id': item_id,
                'nome': item.nome,
                'quantidade': quantidade,
                'preco_unitario': item.preco,
                'valor_total': item.preco * quantidade
            })
            session[carrinho_key] = carrinho  # Salva o carrinho

            flash(f"{item.nome} x{quantidade} adicionado ao carrinho!", "alert-success")
            return redirect(url_for('menu'))
        else:
            flash("Erro ao adicionar item ao carrinho.", "alert-danger")

    return render_template(
        'menu.html',
        pratos=pratos,
        sobremesas=sobremesas,
        bebidas=bebidas,
        form_quantidade=form_quantidade
    )



import uuid  # Certifique-se de ter isso no topo do arquivo

@app.route('/carrinho', methods=['GET', 'POST'])
@login_required
def carrinho():
    carrinho_key = f"carrinho_{current_user.id}"
    carrinho = session.get(carrinho_key, [])

    if request.method == 'POST':
        if carrinho:
            codigo_pedido = str(uuid.uuid4())[:8]

            for item in carrinho:
                pedido = Pedido(
                    codigo_pedido=codigo_pedido,
                    id_item=item['item_id'],
                    nome_item=item['nome'],
                    quantidade_item=item['quantidade'],
                    preco_item=item['preco_unitario'],
                    valor_total=item['valor_total'],
                    id_usuario_pedido=current_user.id,
                    status='preparando'  # já define status ao salvar
                )
                database.session.add(pedido)

            database.session.commit()

            # 👉 Armazena os dados do carrinho para exibir no pagamento
            session['dados_pagamento'] = {
                'itens': carrinho,
                'total_geral': sum(item['valor_total'] for item in carrinho)
            }

            session[carrinho_key] = []  # Limpa carrinho apenas desse usuário

            flash(f"Pedido finalizado com sucesso! Código do pedido: {codigo_pedido}", "alert-success")
            return redirect(url_for('pagamento'))
        else:
            flash("Carrinho vazio!", "warning")

    total_geral = sum(item['valor_total'] for item in carrinho)
    return render_template('carrinho.html', carrinho=carrinho, total_geral=total_geral)



@app.route('/pagamento', methods=['GET', 'POST'])
@login_required
def pagamento():
    dados_pagamento = session.get('dados_pagamento')

    if not dados_pagamento:
        flash("Nenhum pedido encontrado para pagamento.", "alert-warning")
        return redirect(url_for('menu'))

    carrinho = dados_pagamento['itens']
    total_geral = dados_pagamento['total_geral']

    if request.method == 'POST':
        forma_pagamento = request.form.get('forma_pagamento')

        if forma_pagamento in ['debito', 'credito']:
            numero_cartao = request.form.get('numero_cartao')
            validade = request.form.get('validade')
            cvv = request.form.get('cvv')

            if not all([numero_cartao, validade, cvv]):
                flash("Por favor, preencha todos os dados do cartão.", "alert-danger")
                return redirect(url_for('pagamento'))

        # ✅ limpa os dados após o pagamento
        session.pop('dados_pagamento', None)

        flash("Pagamento realizado com sucesso!", "alert-success")
        return redirect(url_for('home'))

    return render_template('pagamento.html', carrinho=carrinho, total_geral=total_geral)

@app.route('/meus-pedidos')
@login_required
def meus_pedidos():
    if current_user.tipo != 'cliente':
        flash("Acesso restrito a clientes!", "alert-danger")
        return redirect(url_for('home'))

    pedidos = (
        database.session.query(Pedido)
        .filter_by(id_usuario_pedido=current_user.id)
        .order_by(Pedido.data_criacao.desc())
        .all()
    )

    # Agrupar por código do pedido
    pedidos_agrupados = {}
    for pedido in pedidos:
        pedidos_agrupados.setdefault(pedido.codigo_pedido, []).append(pedido)

    return render_template('meus-pedidos.html', pedidos_agrupados=pedidos_agrupados)



@app.route('/remover-item', methods=['POST'])
@login_required
def remover_item_carrinho():
    item_id = request.form.get('item_id')
    carrinho_key = f"carrinho_{current_user.id}"
    carrinho = session.get(carrinho_key, [])

    carrinho = [item for item in carrinho if item['id'] != item_id]

    session[carrinho_key] = carrinho
    flash("Item removido do carrinho.", "alert-danger")
    return redirect(url_for('carrinho'))



@app.route('/contatos')
def contatos():
    return render_template('contatos.html')



@app.route('/inserir-pratos', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.tipo != 'funcionario':
        flash("Acesso restrito a funcionários!", "alert-danger")
        return redirect(url_for('home'))
    form_prato = FormPrato()
    form_sobremesa = FormSobremesa()
    form_bebida = FormBebida()
    if form_prato.validate_on_submit and 'botao_submit_prato' in request.form:
        prato = Prato(nome = form_prato.nome_prato.data, preco = form_prato.preco_prato.data, ingrediente = form_prato.ingredientes_prato.data)
        database.session.add(prato)
        database.session.commit()
        flash(f'Prato: {form_prato.nome_prato.data} adicionada com sucesso', 'alert-success')
        form_prato.nome_prato.data = None
        form_prato.preco_prato.data = None
        form_prato.ingredientes_prato.data = None

        
    
    if form_sobremesa.validate_on_submit and 'botao_submit_sobremesa' in request.form:
        sobremesa = Sobremesa(nome = form_sobremesa.nome_sobremesa.data, preco = form_sobremesa.preco_sobremesa.data, ingrediente = form_sobremesa.ingredientes_sobremesa.data)
        database.session.add(sobremesa)
        database.session.commit()
        flash(f'Sobremesa: {form_sobremesa.nome_sobremesa.data} adicionada com sucesso', 'alert-success')
        form_sobremesa.nome_sobremesa.data = None
        form_sobremesa.preco_sobremesa.data = None
        form_sobremesa.ingredientes_sobremesa.data = None

    
    if form_bebida.validate_on_submit and 'botao_submit_bebida' in request.form:
        bebida = Bebida(nome = form_bebida.nome_bebida.data, preco = form_bebida.preco_bebida.data, teor_alcoolico = form_bebida.teor_alcoolico.data)
        database.session.add(bebida)
        database.session.commit()
        flash(f'Bebida: {form_bebida.nome_bebida.data} adicionada com sucesso', 'alert-success')
        form_bebida.nome_bebida.data = None
        form_bebida.preco_bebida.data = None
        form_bebida.teor_alcoolico.data = None
        
        


    return render_template('inserir-pratos.html', form_prato=form_prato, form_sobremesa=form_sobremesa, form_bebida=form_bebida)

@app.route('/apagar-pratos', methods=['GET', 'POST'])
@login_required
def admin2():
    if current_user.tipo != 'funcionario':
        flash("Acesso restrito a funcionários!", "alert-danger")
        return redirect(url_for('home'))
    
    form_excluir = FormExcluir()

    # Defina as variáveis antes da lógica do formulário
    lista_pratos = Prato.query.all()
    pratos = [
        {"id": prato.id_prato, "nome": prato.nome, "preco": prato.preco, "ingrediente": prato.ingrediente}
        for prato in lista_pratos
    ]

    lista_sobremesas = Sobremesa.query.all()
    sobremesas = [
        {"nome": sobremesa.nome, "preco": sobremesa.preco, "ingrediente": sobremesa.ingrediente}
        for sobremesa in lista_sobremesas
    ]

    lista_bebidas = Bebida.query.all()
    bebidas = [
        {"nome": bebida.nome, "preco": bebida.preco, "teor_alcoolico": bebida.teor_alcoolico}
        for bebida in lista_bebidas
    ]

    if form_excluir.validate_on_submit() and 'botao_submit_excluir' in request.form:
        nome_item = form_excluir.nome.data.strip()

        prato = Prato.query.filter_by(nome=nome_item).first()
        sobremesa = Sobremesa.query.filter_by(nome=nome_item).first()
        bebida = Bebida.query.filter_by(nome=nome_item).first()

        if prato:
            database.session.delete(prato)
            database.session.commit()
            flash(f'Prato "{nome_item}" excluído com sucesso!', 'alert-success')
        elif sobremesa:
            database.session.delete(sobremesa)
            database.session.commit()
            flash(f'Sobremesa "{nome_item}" excluída com sucesso!', 'alert-success')
        elif bebida:
            database.session.delete(bebida)
            database.session.commit()
            flash(f'Bebida "{nome_item}" excluída com sucesso!', 'alert-success')
        else:
            flash(f'Nenhum item encontrado com o nome "{nome_item}".', 'alert-danger')

        # Atualize as listas após a exclusão
        lista_pratos = Prato.query.all()
        pratos = [
            {"id": prato.id, "nome": prato.nome, "preco": prato.preco, "ingrediente": prato.ingrediente}
            for prato in lista_pratos
        ]

        lista_sobremesas = Sobremesa.query.all()
        sobremesas = [
            {"nome": sobremesa.nome, "preco": sobremesa.preco, "ingrediente": sobremesa.ingrediente}
            for sobremesa in lista_sobremesas
        ]

        lista_bebidas = Bebida.query.all()
        bebidas = [
            {"nome": bebida.nome, "preco": bebida.preco, "teor_alcoolico": bebida.teor_alcoolico}
            for bebida in lista_bebidas
        ]

        return redirect(url_for('admin2'))

    return render_template('apagar-pratos.html', form_excluir=form_excluir, pratos=pratos, sobremesas=sobremesas, bebidas=bebidas)

@app.route('/controle-pedidos', methods=['GET', 'POST'])
@login_required
def controle_pedidos():
    if current_user.tipo != 'funcionario':
        flash("Acesso restrito!", "alert-danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        codigo = request.form.get('codigo_pedido')
        if codigo:
            pedidos = Pedido.query.filter_by(codigo_pedido=codigo).all()
            for pedido in pedidos:
                pedido.status = 'pronto'
            database.session.commit()
            flash(f"Pedido {codigo} marcado como pronto!", "alert-success")
        return redirect(url_for('controle_pedidos'))

    # Agrupar por código_pedido
    codigos_preparando = (
        database.session.query(Pedido.codigo_pedido)
        .filter_by(status='preparando')
        .distinct()
        .order_by(Pedido.data_criacao.asc())
        .all()
    )
    codigos_prontos = (
        database.session.query(Pedido.codigo_pedido)
        .filter_by(status='pronto')
        .distinct()
        .order_by(Pedido.data_criacao.asc())
        .all()
    )

    pedidos_preparando = [
        database.session.query(Pedido).filter_by(codigo_pedido=cp.codigo_pedido).all()
        for cp in codigos_preparando
    ]
    pedidos_prontos = [
        database.session.query(Pedido).filter_by(codigo_pedido=cp.codigo_pedido).all()
        for cp in codigos_prontos
    ]

    return render_template(
        'controle-pedidos.html',
        pedidos_preparando=pedidos_preparando,
        pedidos_prontos=pedidos_prontos
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # Login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # Procura na tabela Usuario (base para Cliente e Funcionario)
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        
        # Verifica se o usuário foi encontrado e se a senha está correta
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)

            # Flash message com base no tipo do usuário
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        
        else:
            flash('Falha no login. Email ou Senha incorretos', 'alert-danger')

    # Criar Conta
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')

        # Cria um cliente (pode ser ajustado se também quiser criar funcionários)
        cliente = Cliente(
            nome=form_criarconta.nome.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )
        database.session.add(cliente)
        database.session.commit()

        flash(f'Conta criada com sucesso no e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    session.pop(f'carrinho_{current_user.id}', None)
    logout_user()
    return redirect(url_for('home'))





