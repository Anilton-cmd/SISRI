import psycopg2


def conectar():

    try:

        conexao = psycopg2.connect(

            database="sisri_cv",

            user="postgres",

            password="AMG25.com",

            host="localhost",

            port="5432"

        )


        print("Conexão com PostgreSQL realizada com sucesso")


        return conexao


    except Exception as erro:


        print("Erro na conexão:", erro)