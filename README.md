# 🍝 Tô com Fome - Sistema Web de Pedidos para Restaurante

Este é um sistema completo para gerenciamento de pedidos de um restaurante, desenvolvido com **Flask**. A aplicação oferece funcionalidades para clientes realizarem pedidos, funcionários gerenciarem o cardápio e controlarem o andamento dos pedidos.

## 🚀 Funcionalidades

### 👥 Autenticação
- Cadastro e login de **clientes** e **funcionários**
- Sistema de sessão com Flask-Login

### 🍽️ Cardápio Dinâmico
- Visualização de **pratos**, **sobremesas** e **bebidas**
- Adição de itens ao **carrinho** com controle de quantidade
- Exclusão de itens do cardápio (restrito a funcionários)

### 🛒 Carrinho e Pedidos
- Carrinho individual por cliente (com uso de `session`)
- Geração de pedidos com **UUID** como código único
- Histórico completo de pedidos com status e totalizador

### 💳 Pagamento
- Simulação de pagamento com opções: **Crédito**, **Débito**, **Pix**, **Dinheiro**
- Formulários adaptáveis via JavaScript
- Geração de QR Code para pagamento via Pix (imagem estática)

### 📦 Controle de Pedidos
- Painel administrativo para funcionários:
  - Visualizar pedidos em **preparação** ou **prontos**
  - Marcar pedidos como prontos

### 📱 Contato
- Página com botões de acesso direto para:
  - Email
  - WhatsApp
  - Instagram
  - Telefone

---

## 🧠 Tecnologias Utilizadas

- **Python 3.11
- **Flask**
- **Flask-WTF** (validação de formulários)
- **Flask-Login** (autenticação)
- **Flask-Bcrypt** (hash de senha)
- **SQLAlchemy** + **SQLite** (ORM e banco local)
- **Bootstrap 5.3** (interface responsiva)
- HTML, Jinja2, CSS (via Bootstrap)

---

## 🔒 Usuários de Teste

| Tipo        | Email                   | Senha   |
|-------------|--------------------------|---------|
| 🧍 Cliente  | teste1@gmail.com        | 123456  |
| 🛠️ Funcionário | admin@gmail.com     | admin123  |

