# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from funcoes.Serializador import serialize_data, serialize_split_num_part

class JobartiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VagasItem(scrapy.Item):
    # item para as vagas de trabalho
    id_vaga = scrapy.Field()
    cargo = scrapy.Field()
    setor = scrapy.Field()
    contrato = scrapy.Field()
    titulacao = scrapy.Field()
    experiencia = scrapy.Field(serializer = serialize_split_num_part)
    nacionalidade = scrapy.Field()
    lingua = scrapy.Field()
    area = scrapy.Field()
    ano = scrapy.Field(serializer = serialize_data)

class CompetenciasItem(scrapy.Item):
    # item para as competencias do funcionario na empresa
    id_competencia = scrapy.Field()
    competencia = scrapy.Field()

class RequisitosItem(scrapy.Item):
    # item para os requisitos ou aptidões que o funcionario deve ter para ser aceito na vaga
    id_requisitos = scrapy.Field()
    requisitos = scrapy.Field()