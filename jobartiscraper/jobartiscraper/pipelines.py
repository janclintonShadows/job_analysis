# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exporters import CsvItemExporter
# from jobartiscraper.items import VagasItem, CompetenciasItem, RequisitosItem
from scrapy.exceptions import DropItem
from datetime import datetime as dt

class JobartiscraperPipeline:
    def process_item(self, item, spider):

        if 'ano' in item:
            data_atual = dt.today()
            data = dt.strptime(item['ano'],r'%d/%m/%Y')
            if data > data_atual:
                item['ano'] = data.year - (data.year - data_atual.year)
            else:
                item['ano'] = data.year

            if 'nenhum' in item['experiencia'].lower():
                item['experiencia'] = 0
            else:
                item['experiencia'] = item['experiencia'].split(' ')[0]

        return item
        
        
# class MultiCSVItemPipeline:
#     def open_spider(self, spider):
#         self.files = {
#             'vaga': open('vagas.csv', 'wb'),
#             'competencia': open('competencias.csv', 'wb'),
#             'requisitos': open('requisitos.csv', 'wb')
#         }
#         self.exporters = {
#             'vaga': CsvItemExporter(self.files['vaga']),
#             'competencia': CsvItemExporter(self.files['competencia']),
#             'requisitos': CsvItemExporter(self.files['requisitos'])
#         }
#         for exporter in self.exporters.values():
#             exporter.start_exporting()
    
#     def close_spider(self, spider):
#         for exporter in self.exporters.values():
#             exporter.finish_exporting()
#         for file in self.files.values():
#             file.close()

#     def process_item(self, item, spider):
#         if isinstance(item, VagasItem):
#             self.exporters['vaga'].export_item(item)
#         elif isinstance(item, CompetenciasItem):
#             self.exporters['competencia'].export_item(item)
#         elif isinstance(item, RequisitosItem):
#             self.exporters['requisitos'].export_item(item)
#         return item


class MySQLDB2Pipeline:

    def open_spider(self, spider):
        self.con = mysql.connector.connect(
            host = 'localhost', 
            user='root', 
            password ='', 
            database='emprego'
        )
        self.cur = self.con.cursor()


    def close_spider(self, spider):
        self.cur.close()
        self.con.close()


    def process_item(self, item, spider):
        # Adicionando vagas no BD
        query = """
        INSERT INTO vagas (cargo, setor, tipo_de_contrato, experiencia, nacionalidade, lingua, area, ano, titulacao
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        self.cur.execute(query,(item['cargo'],item['setor'],item['contrato'],item['experiencia'],item['nacionalidade'],item['lingua'],item['area'],item['ano'],item['titulacao']))
         
        self.con.commit()
         # pegando o id criado automaticamente e salvando no Item ID
        item['id'] = self.cur.lastrowid

        for competencia in item['competencia']:
            # Inserindo dados na tabela competencia e tabela vaga_competencia
            query = """
             INSERT INTO competencia (competencia
             ) VALUES (%s);
                """
            self.cur.execute(query,(competencia,))
            self.con.commit()

             # Pegando os ids e adicionando os elementos na tabela vaga_competencia
             # apagar desde a linha 38.
            id = self.cur.lastrowid
            query = """
             INSERT INTO vaga_competencia (id_vaga, id_compentecia
             ) VALUES (%s,%s);
             """
            self.cur.execute(query,(item['id'],id))
            self.con.commit()

        # criando loop para adicionar cada requitiso, e pegar os ids da tabela.
        for requisito in item['requisitos']:
            query = """
            INSERT INTO requisitos (requisitos
            ) VALUES (%s);
            """

            self.cur.execute(query,(requisito,))
            self.con.commit()
            id = self.cur.lastrowid

            # Salvando dados no banco vaga_requisitos
            query = """
            INSERT INTO vaga_requisitos (id_vaga, id_requisitos
            ) VALUES (%s,%s);
            """
            self.cur.execute(query,(item['id'],id))
            self.con.commit()

        return item
