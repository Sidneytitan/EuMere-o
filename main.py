import streamlit as st
from pymongo import MongoClient

# Função para conectar ao MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://sidneycko:titanbetty@cluster0.feenv6t.mongodb.net/?retryWrites=true&w=majority")
    db = client["EuMereço"]
    collection = db["lista_produto"]
    return collection

# Função para buscar todos os produtos cadastrados no MongoDB
def buscar_produtos(collection):
    produtos = list(collection.find())  # Convertendo o cursor para uma lista de dicionários
    return produtos

# Função para inserir um novo produto no MongoDB
def inserir_produto(collection, nome, valor, quantidade_gramas):
    novo_produto = {"nome": nome, "valor": valor, "quantidade_gramas": quantidade_gramas}
    collection.insert_one(novo_produto)

# Função para atualizar um produto no MongoDB
def atualizar_produto(collection, id_produto, novo_valor):
    collection.update_one({"_id": id_produto}, {"$set": novo_valor})

# Interface de usuário com Streamlit
def main():
    logo_url = "https://raw.githubusercontent.com/Sidneytitan/EuMere-o/main/Logo%20eu%20mere%C3%A7o.jpeg"
    logo_size = (150, 40)  # Tamanho da imagem (largura, altura)
    st.image(logo_url, width=logo_size[0])
    st.header('Produtos Cadastrados', divider='rainbow')

    collection = connect_to_mongodb()

    menu = ["Cadastro de Produto", "Visualizar Produtos", "Atualizar Valor do Produto"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Cadastro de Produto":
        st.subheader("Cadastro de Produto")
        nome = st.text_input("Nome do produto")
        valor = st.number_input("Valor do produto", value=0)
        quantidade_gramas = st.number_input("Quantidade em gramas", value=0)

        if st.button("Cadastrar"):
            inserir_produto(collection, nome, valor, quantidade_gramas)
            st.success("Produto cadastrado com sucesso!")

    elif choice == "Visualizar Produtos":
        st.subheader("Visualizar Produtos")

        produtos = buscar_produtos(collection)

        if produtos:
            st.write("Produtos Cadastrados:")
            for produto in produtos:
                st.write("---")
                st.write(f"**Nome:** {produto['nome']}")
                st.write(f"**Valor:** R${produto['valor']:.2f}")
                st.write(f"**Quantidade em Gramas:** {produto['quantidade_gramas']}")
                st.write("---")
        else:
            st.write("Nenhum produto cadastrado.")

    elif choice == "Atualizar Valor do Produto":
        st.subheader("Atualizar Valor do Produto")

        produtos = buscar_produtos(collection)
        nomes_produtos = [produto['nome'] for produto in produtos]

        if nomes_produtos:
            produto_selecionado_nome = st.selectbox("Selecione um produto para atualizar o valor", nomes_produtos)
            novo_valor = st.number_input("Novo valor do produto")

            if st.button("Atualizar"):
                produto = next((p for p in produtos if p['nome'] == produto_selecionado_nome), None)
                if produto:
                    id_produto = produto["_id"]
                    novo_valor_produto = {"valor": novo_valor}
                    atualizar_produto(collection, id_produto, novo_valor_produto)
                    st.success("Valor do produto atualizado com sucesso!")
        else:
            st.write("Nenhum produto cadastrado.")

if __name__ == "__main__":
    main()
