# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exporters import CsvItemExporter
from jobartiscraper.items import VagasItem, CompetenciasItem, RequisitosItem
from scrapy.exceptions import DropItem

class JobartiscraperPipeline:
    def process_item(self, item, spider):
        return item



class MultiCSVItemPipeline:
    def open_spider(self, spider):
        self.files = {
            'vaga': open('vagas.csv', 'wb'),
            'competencia': open('competencias.csv', 'wb'),
            'requisitos': open('requisitos.csv', 'wb')
        }
        self.exporters = {
            'vaga': CsvItemExporter(self.files['vaga']),
            'competencia': CsvItemExporter(self.files['competencia']),
            'requisitos': CsvItemExporter(self.files['requisitos'])
        }
        for exporter in self.exporters.values():
            exporter.start_exporting()
    
    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
        for file in self.files.values():
            file.close()

    def process_item(self, item, spider):
        if isinstance(item, VagasItem):
            self.exporters['vaga'].export_item(item)
        elif isinstance(item, CompetenciasItem):
            self.exporters['competencia'].export_item(item)
        elif isinstance(item, RequisitosItem):
            self.exporters['requisitos'].export_item(item)
        return item

class MySQLDBPipeline:

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
        if isinstance(item, VagasItem): 
            self.save_vagas(item) 
        elif isinstance(item, CompetenciasItem): 
            self.save_competencias(item) 
        elif isinstance(item, RequisitosItem): 
            self.save_requisitos(item) 
        else: 
            raise DropItem(f"Item desconhecido: {item}") 
        return item
    
    def save_vagas(self, item):
        query = """
        INSERT INTO vagas (cargo, setor, tipo_de_contrato, experiencia. nacionalidade, lingua, area, ano, titulacao
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        self.cur.execute(query,(item['cargo'],item['setor'],item['contrato'],item['experiencia'],item['nacionalidade'],item['lingua'],item['are'],item['ano'],item['titulacao']))
        
        self.con.commit()
        # pegando o id criado automaticamente e salvando no Item ID
        item['id_vaga'] = self.cur.lastrowid

    def save_competencias(self,item):
        query = """
        INSERT INTO competencia (competencia
        ) VALUES (%s)
        """
        self.cur.execute(query,(item['competencia'],))
        self.con.commit()
        # pegando o id criado automaticamente e salvando no Item ID
        item['id_competencia'] = self.cur.lastrowid

        # salvando na tabela de relação com o id Vaga
        if 'id_vaga' in item:
            query = """
            INSERT INTO vaga_compentecia (id_vaga, id_compentecia
            ) VALUES (%s,%s)
            """
            self.cur.execute(query,(item['id_vaga'],item['id_competencia']))
            self.con.commit()

    def save_requisitos(self,item):
        query = """
        INSERT INTO requisitos (requisitos
        ) VALUES (%s)
        """
        self.cur.execute(query,(item['competencia'],))
        self.con.commit()
        # pegando o id criado automaticamente e salvando no Item ID
        item['id_requisitos'] = self.cur.lastrowid

        # salvando na tabela de relação com o id Vaga
        if 'id_vaga' in item:
            query = """
            INSERT INTO vaga_requisitos (id_vaga, id_requisitos
            ) VALUES (%s,%s)
            """
            self.cur.execute(query,(item['id_vaga'],item['id_requisitos']))
            self.con.commit()
