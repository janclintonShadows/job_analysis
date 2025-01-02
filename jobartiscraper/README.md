# JobArtisScraper

![jobastis image](../imgs/jobartis_page.png)

## Introdução

Este projeto contém um webscraper desenvolvido em Python, utilizando a biblioteca Scrapy, com o objetivo de coletar dados de vagas de emprego do site JobArtis.com. As informações extraídas são armazenadas em um banco de dados para posterior análise e utilização. Este projeto pode ser útil para quem deseja realizar análises de mercado de trabalho, monitorar novas oportunidades de emprego ou construir sistemas de recomendação de vagas.

## Funcionalidades

- Extração de dados de vagas de emprego da página JobArtis.com.
- Armazenamento dos dados extraídos em um banco de dados MySQL.
- Suporte a múltiplas categorias e atributos de vagas, incluindo cargo, setor, tipo de contrato, ano disponivel da vaga, titulação mínima, experiência, nacionalidade, línguas, área funcional, competências e requisitos.

## Estrutura do Projeto

- `items.py`: Definição dos itens (dados) que serão extraídos pelo scraper.
- `middlewares.py`: Configuração dos middlewares do Scrapy (se necessário).
- `pipelines.py`: Configuração dos pipelines de processamento e armazenamento dos dados no banco de dados.
- `settings.py`: Configurações do Scrapy, incluindo parâmetros de conexão com o banco de dados.
- `spiders/jobartis.py`: Diretório contendo os spiders responsáveis pela coleta dos dados do site JobArtis.com.
- `README.md`: Documentação do projeto.

## Requisitos

- Python 3.x
- Scrapy
- MySQL
- Biblioteca `mysql` para conexão com o MySQL

## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/janclintonShadows/job_analysis.git
    cd jobartisscraper
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv env
    source env/bin/activate  # No Windows: env\Scripts\activate
    ```

3. Instale as dependências:

    ```bash
    pip install -r /outros/requirements.txt
    ```

4. Configure o banco de dados MySQL:

    - Crie um banco de dados no MySQL.
    - Atualize as configurações de conexão no arquivo `settings.py`.

## Uso

1. Navegue até o diretório do projeto:

    ```bash
    cd jobartiscraper
    ```

2. Execute o spider para iniciar a coleta de dados:

    ```bash
    scrapy crawl jobartis
    ```

3. Os dados serão armazenados no banco de dados MySQL conforme configurado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.
