from database.conexao import conectar


conexao = conectar()


if conexao:

    print("Banco SISRI conectado")

    conexao.close()