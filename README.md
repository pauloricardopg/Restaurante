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

- **Python 3.11**
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
| 🧍 Cliente  | pr@gmail.com        | 123456  |
| 🛠️ Funcionário | admin@gmail.com     | admin123  |

---

## 📸 Layout (Exemplos)

### 🔐 Tela de Login e Criação de Conta
![LoginECriarConta](https://github.com/user-attachments/assets/dafdcc5c-bc0f-4286-8cad-66a9a840e1a0)

---

### 🍽️ Cardápio com Pratos, Sobremesas e Bebidas
![Cardapio](https://github.com/user-attachments/assets/2b86c0ae-fa9f-4d07-8ddb-fc2ac10242d6)

---

### 🛒 Carrinho de Compras
![Carrinho](https://github.com/user-attachments/assets/0bd1ad85-8847-4db7-bf6d-2e0c8f8d6382)

---

### 💳 Tela de Pagamento
![Pagamento](https://github.com/user-attachments/assets/daa4bcdf-a81a-43f3-9e67-5d507c00505e)

---

### 📦 Histórico do Cliente - Meus Pedidos
![MeusPedidos](https://github.com/user-attachments/assets/77890853-9e34-46e8-a529-bc75a067f878)

---
 
### ➕ Inserção de Pratos, Sobremesas e Bebidas (funcionário)
![InserirProdutos](https://github.com/user-attachments/assets/2e20a1c2-77b5-40ce-b707-9a2f0dc62cc8)

---

### ❌ Exclusão de Itens do Cardápio (funcionário)
![ApagarProdutos](https://github.com/user-attachments/assets/98fdf152-ced3-4c2e-9f12-41192d2dee6b)

---

### 🧑‍🍳 Painel de Controle de Pedidos (funcionário)
![Controle de pedidos](https://github.com/user-attachments/assets/25197b93-4657-4293-91f4-c2ae07e547b9)



















