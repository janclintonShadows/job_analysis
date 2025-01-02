from testador import MySQL_conecction

db = MySQL_conecction('testes')

# valos inserir valor ao banco de dados
dic = {
    'col_1':'funcionou',
    'col_2': 'perfeitamente'
}
db.inserir_valores('teste_1',dic)
db.close()
