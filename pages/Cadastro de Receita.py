import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Função para conectar ao MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://sidneycko:titanbetty@cluster0.feenv6t.mongodb.net/?retryWrites=true&w=majority")
    db = client["EuMereço"]
    collection_produto = db["lista_produto"]
    collection_receita = db["lista_receita"]
    return collection_produto, collection_receita

# Função para buscar todos os produtos cadastrados no MongoDB
def buscar_produtos(collection):
    produtos = collection.distinct("nome")
    return produtos

# Função para buscar todas as receitas cadastradas no MongoDB
def buscar_receitas(collection):
    receitas = list(collection.find())
    return receitas

# Função para buscar o custo por grama de um produto
def buscar_custo_por_grama(produto_nome, collection_produto):
    produto = collection_produto.find_one({"nome": produto_nome})
    if produto:
        return produto["valor"] / produto["quantidade_gramas"]
    return 0

# Função para calcular o custo total de um ingrediente
def calcular_custo_total(ingrediente, collection_produto):
    custo_por_grama = buscar_custo_por_grama(ingrediente["nome"], collection_produto)
    return custo_por_grama * ingrediente["quantidade"]

# Função para calcular o valor total da receita
def calcular_valor_total_receita(ingredientes, collection_produto):
    valor_total = 0
    for ingrediente in ingredientes:
        valor_total += calcular_custo_total(ingrediente, collection_produto)
    return valor_total

# Função para inserir uma nova receita no MongoDB
def inserir_receita(collection_receita, nome_receita, ingredientes):
    receita = {"nome": nome_receita, "ingredientes": ingredientes}
    collection_receita.insert_one(receita)

# Interface de usuário com Streamlit
def main():
    logo_url = "https://raw.githubusercontent.com/Sidneytitan/EuMere-o/main/Logo%20eu%20mere%C3%A7o.jpeg"
    logo_size = (150, 40)  # Tamanho da imagem (largura, altura)
    st.image(logo_url, width=logo_size[0])
    st.header('Produtos Cadastrados', divider='rainbow')

    collection_produto, collection_receita = connect_to_mongodb()

    menu = ["Cadastro de Receita", "Visualização de Receitas"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Cadastro de Receita":
        st.subheader("Cadastro de Receita")
        nome_receita = st.text_input("Nome da Receita")
        num_ingredientes = st.number_input("Número de Ingredientes", min_value=1, value=1)

        ingredientes = []
        for i in range(num_ingredientes):
            col1, col2 = st.columns([3, 1])
            with col1:
                ingrediente_nome = st.selectbox(f"Nome do Ingrediente {i+1}", buscar_produtos(collection_produto))
            with col2:
                ingrediente_quantidade = st.number_input(f"Quantidade do Ingrediente {i+1}", min_value=0)
            ingredientes.append({"nome": ingrediente_nome, "quantidade": ingrediente_quantidade})

        if st.button("Cadastrar Receita"):
            inserir_receita(collection_receita, nome_receita, ingredientes)
            st.success("Receita cadastrada com sucesso!")

    elif choice == "Visualização de Receitas":
        st.subheader("Visualização de Receitas")

        receitas = buscar_receitas(collection_receita)
        if len(receitas) == 0:
            st.write("Nenhuma receita cadastrada.")
        else:
            opcoes = [receita['nome'] for receita in receitas]
            receita_selecionada = st.selectbox('Selecione uma receita', opcoes)

            for receita in receitas:
                if receita['nome'] == receita_selecionada:
                    # Calcular e exibir o valor total da receita em um painel separado
                    valor_total_receita = calcular_valor_total_receita(receita["ingredientes"], collection_produto)
                    st.subheader("Valor Total da Receita")
                    st.markdown(f"<div style='background-color:#f0f0f0;padding:10px;border-radius:5px;'><h3 style='text-align:center;color:#1f77b4;'>Valor Total da Receita</h3><h2 style='text-align:center;color:#1f77b4;'>R${valor_total_receita:.2f}</h2></div>", unsafe_allow_html=True)

                    st.write(f"**Detalhes da Receita: {receita['nome']}**")
                    ingredientes = receita["ingredientes"]
                    data = []
                    for ingrediente in ingredientes:
                        custo_total = calcular_custo_total(ingrediente, collection_produto)
                        data.append([ingrediente["nome"], ingrediente["quantidade"], custo_total])
                    st.write(pd.DataFrame(data, columns=["Ingrediente", "Quantidade", "Custo Total"]))

if __name__ == "__main__":
    main()





