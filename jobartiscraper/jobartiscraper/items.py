# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobartiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VagasItem(scrapy.Item):
    # item para as vagas de trabalho
    id = scrapy.Field()
    cargo = scrapy.Field()
    setor = scrapy.Field()
    contrato = scrapy.Field()
    titulacao = scrapy.Field()
    experiencia = scrapy.Field()
    nacionalidade = scrapy.Field()
    lingua = scrapy.Field()
    area = scrapy.Field()
    ano = scrapy.Field()
    competencia = scrapy.Field()
    requisitos = scrapy.Field()

# class CompetenciasItem(scrapy.Item):
#     # item para as competencias do funcionario na empresa
#     id = scrapy.Field()
#     competencia = scrapy.Field()

# class RequisitosItem(scrapy.Item):
#     # item para os requisitos ou aptidões que o funcionario deve ter para ser aceito na vaga
#     id = scrapy.Field()
#     requisitos = scrapy.Field()