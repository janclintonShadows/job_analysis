import scrapy
from jobartiscraper.items import VagasItem, RequisitosItem, CompetenciasItem


class JobartisSpider(scrapy.Spider):
    name = "jobartis"
    allowed_domains = ["www.jobartis.com"]
    start_urls = ["https://www.jobartis.com/vagas-emprego"]

    def parse(self, response):
        # pegando todas as proposta de trabalho da pagina
        jobs = response.xpath('//a[@class="job-link"]')

        # iterando pela lista disponivel de trabalho
        for job in jobs:
            # Vamos pegar os links e clicar sobre ele, e pegar os dados nela contida
            job_url = job.css('a::attr(href)').get()
            # chamar a função parse_job
            yield response.follow(job_url, callback = self.parse_jobs)
        
        # pegar o link de ir para outra pagina
        next_page = response.css('a:contains("Seguinte")::attr(href)').get()
        # Analisar se chegou na ultima pagina
        if next_page is not None:
            if 'https://www.jobartis.com' not in next_page:
                next_page_url = 'https://www.jobartis.com' + next_page
            else:
                next_page_url = 'https://www.jobartis.com' + next_page

            yield response.follow(next_page_url, callback = self.parse)

    def parse_jobs(self, response):
        """
        Função Responsavel por pegar os dados de cada postagem de recrutamento
        """
        vagas = VagasItem() # importando o container de vagas
        

        # vamos salvar os dados correspondente a cada vaga
        vagas['cargo'] = response.xpath('//div[@class="col-sm-9"]')[0].css('::text').get()
        vagas['contrato'] = response.xpath('//div[@class="col-sm-9 col-xs-6"]')[0].css('::text').get()
        vagas['setor'] = response.xpath('//div[@class="col-sm-9"]')[1].css('::text').get()
        vagas['titulacao'] = response.css('div:contains("Titulação mínima"):nth-child(7) > div.col-md-9.col-xs-6::text').get()
        vagas['experiencia'] = response.css('div:contains("Experiência exigida") > div.col-md-9.col-xs-6::text').get()
        vagas['nacionalidade'] = response.css('div:contains("Nacionalidade") > div.col-md-9.col-xs-6::text').get()
        vagas['lingua'] = response.css('div:contains("Línguas") > div.col-md-9.col-xs-6::text').get()
        vagas['area'] = response.css('div.col-md-9.col-sm-12 > a::text').get()
        vagas['ano'] = response.xpath('//div[@class="col-sm-9 col-xs-6"]')[1].css('::text').get()

        # Vamos guardar os dados para cada competencia
        for comp in response.css('div.col-md-9.col-sm-12  li'):
            competencia = CompetenciasItem()
            competencia['competencia'] = comp.css('::text').get()
            competencia['id_vaga'] = vagas['id']
            yield competencia

        # vamos guardar os dados para cada requisitos
        for req in response.xpath('//*[@id="main-container"]/div/div[1]/div[3]/div[2]/div[11]/div[2]/p').css('::text'):
            requisitos = RequisitosItem()
            requisitos['requisitos'] = req.get()
            requisitos['id_vaga'] = vagas['id']
            yield requisitos

        
        # retornando as vagas
        yield vagas