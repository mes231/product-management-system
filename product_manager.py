"""
Documentação do Sistema de Cadastro e Listagem de Produtos

Este sistema é desenvolvido em Python utilizando a biblioteca Tkinter para a interface gráfica do usuário (GUI) e SQLite para a persistência de dados. Ele permite o cadastro de produtos com nome, descrição, valor e disponibilidade, além de oferecer funcionalidades de listagem completa e listagem ordenada por valor.

Ferramentas Utilizadas:
- Python: Linguagem de programação principal.
- Tkinter: Biblioteca padrão do Python para criação de interfaces gráficas.
- SQLite: Sistema de gerenciamento de banco de dados embutido no Python para armazenamento dos dados.
- ttk (Tkinter Treeview): Utilizado para exibir dados em forma de tabelas.

Funcionalidades:
1. Cadastro de Produtos: Permite a inserção de novos produtos no banco de dados com campos para nome, descrição, valor e disponibilidade.
2. Listagem Completa: Exibe todos os produtos cadastrados em uma interface separada, com todas as informações detalhadas.
3. Listagem Ordenada por Valor: Apresenta uma listagem reduzida dos produtos, ordenada pelo valor, exibindo apenas o nome e o valor do produto.

Organização do Código:
- Conexão com o banco de dados SQLite.
- Definição de funções principais para manipulação dos produtos (cadastro e listagem).
- Configuração e apresentação da interface gráfica com campos de entrada, rótulos e botões de ação.
- Uso de Treeview para exibição dos produtos cadastrados.

Como Utilizar:
1. Execute o script Python para abrir a interface do sistema.
2. Preencha os campos de nome, descrição, valor e disponibilidade para cadastrar um novo produto.
3. Utilize os botões para acessar as funcionalidades de listagem completa ou listagem ordenada por valor.

Observações:
- Certifique-se de que o arquivo 'database.db' está no mesmo diretório do script ou será criado automaticamente.
- As alterações no banco de dados são persistidas imediatamente após cada operação de cadastro.

Este sistema é uma solução básica para gerenciamento de produtos e pode ser expandido com funcionalidades adicionais conforme necessário.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Conexão com o banco de dados SQLite
# ----------------------------------------------------------------------------
database = sqlite3.connect("database.db")

cursor = database.cursor()

# Criação da tabela de produtos caso não exista
cursor.execute("CREATE TABLE IF NOT EXISTS produtos (nome TEXT, descricao TEXT, valor TEXT, disponivel TEXT)")

# Função para listar todos os produtos em uma nova tela
# ----------------------------------------------------------------------------
def list_products():
    # Configuração do frame de listagem
    listing_frame.place(relheight=1, relwidth=1)

    # Seleciona todos os produtos do banco de dados
    products = cursor.execute("SELECT * FROM produtos")

    # Remove todos os itens existentes na Treeview
    for item in listing.get_children():
        listing.delete(item)
    
    # Configura as colunas da Treeview de listagem
    listing.column('nome', width=120)
    listing.column('descricao', width=200)
    listing.column('valor', width=90)
    listing.column('disponivel', width=90)

    # Insere cada produto na Treeview
    for p in products:
        listing.insert('', 'end', values=p)

    # Exibe a Treeview e o botão de voltar
    listing.place(x=100, y=50, width=800)

    backHomeBt = tk.Button(listing_frame, text="Voltar", command= lambda: listing_frame.place_forget())
    backHomeBt.place(x=1, y=1)

# Função para listar produtos ordenados por valor (colunas específicas)
# ----------------------------------------------------------------------------
def collumnListingProducts():
    # Seleciona os produtos ordenados pelo valor convertido para REAL
    products = cursor.execute("SELECT * FROM produtos ORDER BY CAST(valor AS REAL) ASC")

    # Remove todos os itens existentes na Treeview
    for item in collumnListing.get_children():
        collumnListing.delete(item)
    
    # Configura as colunas da Treeview de listagem reduzida
    collumnListing.column('nome', width=120)
    collumnListing.column('valor', width=100)

    # Insere cada produto na Treeview com nome e valor
    for p in products:
        collumnListing.insert('', 'end', values=(p[0], p[2]))
    collumnListing.place(x=800, y=200, width=400)

# Função para registrar um novo produto
# ----------------------------------------------------------------------------
def register():
    # Obtém os dados dos campos de entrada
    productName = name.get().strip().title()
    productDescription = description.get().strip().title()
    productValue = value.get().replace(',', '.').strip()
    productAvailable = available.get().title()

    # Verifica se todos os campos estão preenchidos corretamente
    if productName and productDescription and productValue and productAvailable in ["Sim","Não"]:
        try:
            # Tenta converter o valor para float
            productValue = float(productValue)
        except:
            # Exibe mensagem de erro se a conversão falhar
            messagebox.showerror("Erro", "Valor inválido!")
        else:
            # Insere o produto no banco de dados
            cursor.execute("INSERT INTO produtos (nome, descricao, valor, disponivel) VALUES (?, ?, ?, ?)", (productName, productDescription, productValue, productAvailable,))
            
            # Limpa os campos de entrada
            name.delete(0, tk.END)
            description.delete(0, tk.END)
            value.delete(0, tk.END)
            available.set('')
            
            # Confirma a operação no banco de dados
            database.commit()
            messagebox.showinfo("Concluído", "Produto adicionado com sucesso!")
    else:
        # Exibe mensagem de erro se algum campo estiver incorreto
        messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
    
    # Atualiza a listagem reduzida de produtos
    collumnListingProducts()

# Configuração inicial do Tkinter
# ----------------------------------------------------------------------------
app = tk.Tk()
app.title("Cadastro e listagem de produtos")
app.geometry("900x500")

# Campos de entrada e rótulos para registro de produtos
# ----------------------------------------------------------------------------
nameLb = tk.Label(app, text= "Nome do Produto:")
nameLb.place(x=60,y=60)
name = tk.Entry(app, width=30)
name.place(x=200,y=60)

descriptionLb = tk.Label(app, text= "Descrição do Produto:")
descriptionLb.place(x=60,y=100)
description = tk.Entry(app, width=60)
description.place(x=200,y=100)

valueLb = tk.Label(app, text="Valor do produto:")
valueLb.place(x=600,y=60)
value = tk.Entry(app)
value.place(x=700,y=60)

availableLb = tk.Label(app, text="Disponível:")
availableLb.place(x=600,y=100)
available = ttk.Combobox(app, width=30)
available['values'] = ["Sim", "Não"]
available.place(x=700,y=100)

# Treeview para listagem reduzida com Nome e Valor
# ----------------------------------------------------------------------------
collumnListing = ttk.Treeview(app, columns=("nome","valor"), show='headings')
collumnListing.heading('nome', text='Nome do produto', anchor="w")
collumnListing.heading('valor', text='Valor', anchor="w")

# Botões de ação
# ----------------------------------------------------------------------------
registerBt = tk.Button(app, text="Cadastrar", command=register)
registerBt.place(x=200, y=200)

listBt = tk.Button(app, text="Listagem completa", command=list_products)
listBt.place(x=300, y=200)

# Frame e Treeview para listagem completa de produtos
# ----------------------------------------------------------------------------
listing_frame = tk.Frame(app)

listing = ttk.Treeview(listing_frame, columns=("nome","descricao","valor", "disponivel"), show='headings')
listing.heading('nome', text='Nome do produto', anchor='center')
listing.heading('descricao', text='Descrição', anchor='center')
listing.heading('valor', text='Valor', anchor='center')
listing.heading('disponivel', text='Disponível', anchor='center')

# Inicializa a listagem reduzida de produtos
collumnListingProducts()

# Inicia o loop principal do Tkinter
# ----------------------------------------------------------------------------
app.mainloop()
database.close()  # Fecha a conexão com o banco de dados ao finalizar
