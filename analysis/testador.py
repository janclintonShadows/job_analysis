import mysql.connector

class MySQL_conecction:

    def __init__(self,db,host='localhost',user='root',password=''):
        """
    Inicializa o banco de dados, faz a conexão.

    Args: 
        db (str): O nome do banco de dados que se pretentendo conectar.
        host (str='localhost'): O nome do servidor, se for um servidor local, o nome padrão é `localhost`.
        user (str='root'): O nome de usuario do sistema SGBD.
        password (str): A senha do sistma SGBD do usuario correspondente.
    
    Returns: 
        None
    """
        self.con = mysql.connector.connect(
            host = host, user=user, password =password, database=db
        )
        self.cur = self.con.cursor()

    def inserir_valores(self, nome_tabela, valor):
        """
        Insere um valor no banco de dados.

        Args:
            nome_tabela (str): o nome da tabela que se pretende criar;
            valor (**kwargs): Dicionario com nomes correspondentes das colunas e valores que se pretende inserir no banco de dados

        Return None
        """
        if isinstance(valor, dict):
            colunas = ','.join(valor.keys())
            valores = ','.join('%s' for _ in valor.values())
            query = f"""INSERT INTO {nome_tabela}({colunas}) VALUES({valores});
            """
            flag = False
            try:
                self.cur.execute(query,tuple(valor.values()))
                self.con.commit()
            except Exception as e:
                print("Ocorreu um erro {}".format(e))
                flag = True
            finally:
                if flag:
                    self.close()
        else:
            raise TypeError('A variavel não é um dicionario')

    def close(self):
        """Fecha todas as conexões feitas com o banco de dados"""
        self.cur.close()
        self.con.close()