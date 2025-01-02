# __ANALISE EM VAGAS DE EMPREGO__

![The photo was taken from THE DREADED JOB SEARCH and inc.com](/imgs/job_search.png)
[fonte: Job Market Analysis](https://medium.com/sfu-cspmp/job-market-analysis-a905b9a29a31)

## 1. Entendimento do Negócio

O mercado de trabalho é muito competitivo e complicado, especialmente para aqueles que estão fora do mercado de trabalho, ou para quem pretende fazer uma transição.
Sendo que os recrutadores pedem vários requisitos em uma vaga de trabalho, entre eles anos de experiências, formação, habilidades e certificações, saber quais são os requisitos mais frequentemente pedidos para uma categoria ou área, poderia ajudar aqueles fora do mercado laboral, a se prepararem melhor quando forem a se preparar para uma dada vaga.

### __1.1 - Objetivos do Negócio__

Identificar os requisitos importantes que os recrutadores pedem para uma vaga de trabalho de determinada área.

1. Quais habilidades são necessárias para um candidato a emprego entrar em uma carreira?
2. A média de experiência requirida por vaga.
3. Quais competências para determinadas vagas o candidato vai exercer?
4. Quais fatores uma empresa pode melhorar para aumentar o número de candidaturas potenciais e de qualidade?

### __1.2 - Situação Atual__

Os recursos necessários para essa analise são:

- Python;
- SQL;
- Tableau;
- VSCode;
- NLP;
- Muito café e disposição!

Actualmente as pessoas não sabem que requisitos são os mais requeridos pelos recrutadores, e perdem tempo aprendendo varias coisas que podem ser ou não essencial para aumentar a possibilidade de conseguir a tão sonhada vaga de emprego.

Para isso se é requerido que se analise os proposta de empregos disponivel para encontrar pontos e elementos que possam auxiliar as pessoas a focarem naquilo que precisam para cada certas vagas e propostas de trabalho.

Não temos uma fonte de dados disponivel para essa analise, o que vai necessitar que se faça uma colecta de dados em sites de emprego para obteção das informações desejadas. [Webscraping de dados](/jobartiscraper/)

## 2. Entendimento dos Dados

Como não temos dados disponivel, recorremos a metodo de raspagem web ([Webscraping de dados](/jobartiscraper/)), para obtermos os dados para nossa analise.

### __2.1 - Coleta de Dados__

![imagem da pagina inicial da Jobartis](/imgs/jobartis_page.png)

Para esse projecto a fonte de dados escolhida foi a vagas de emprego disponivel no site [jobartis.com](www.jobartis.com). Já que os dados estão melhor organizados em comparação a outros sites de emprego a nivel nacional (Angola), o que facilita e não só extrair os dados, como criar uma estrutura para os tipos de dados que vão ser colectados.

Os dados após a sua extração ([Clique aqui para ver como foi feito a extração e armazenamentod e dados](/jobartiscraper/)), será armazenado em um banco de dados, que terá a seguinte esquematica:

![Imagem da estructura de dados no SGBD](/imgs/db_schema.png)

> Esse esquema foi gerado usando o _web app_ [dbdiagram.io](https://dbdiagram.io/d), na qual você não precisa criar uma conta para poder criar um exemplar de um diagrama de banco de dados, bastando apenas saber escrever código similar ao da criação de tabelas de banco de dados e suas relacões.

```sql
// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

table competencia{
  id interger [primary key]
  competencia text
}

table vagas{
id integer [primary key]
cargo varchar(255)
setor varchar(255)
tipo_de_contrato varchar(50)
experiência integer [null]
nacionalidade varchar(255)
lingua varchar(255)
area varchar(255)
ano integer
titulação varchar(255)
}

table requisitos{
  id integer [primary key]
  requisitos text
}

table vaga_competencia{
  id_vagas integer [not null]
  id_competencia integer [not null]
}

table vaga_requisitos{
  id_vagas integer [not null]
  id_requisitos integer [not null]
}

ref: vagas.id < vaga_competencia.id_vagas // um para muitos
ref: vagas.id < vaga_requisitos.id_vagas
ref: requisitos.id < vaga_requisitos.id_requisitos
ref: competencia.id < vaga_competencia.id_competencia
```

Ou você pode conectar com o teu banco de dados e gerar o diagrama, mas para isso requer que o usuario tenha uma conta no web app.

### __2.2 Exploração dos Dados__

Para a exploração de dados, usamos SQL, sendo que o os dados estão armazenados no banco de dados, podemos usar conjuntos de comandos SQL para selecionar, e explorar o conjunto de dados, uma vez disponivel.

O comando abaixo nos permite selecionar todos os dados (linhas e colunas) da tabela vagas.

```sql
SELECT * FROM vagas;
```

Caso queiramos selecionar somente as vagas para um ano especifico, podemos o usar o `WHERE` e definir um parametro de dados a selecionar, neste exemplo, vamos selecionar apenas as vagas do ano 2024.

```sql
SELECT * FROM vagas WHERE ano = 2024;
```

O que vai nos retornar a seguinte tabela:

de tal modo podemos explorar as outras tabelas, para procurar padrões e anomalias nos dados.

Ou podemos também escrever um Query complexo usando comandos `join` para juntar todos os bancos de dados em apenas um (1), e pegar os valores desejados (colunas ou linhas).

```SQL
SELECT
    v.id AS vaga_id,
    v.cargo,
    v.setor,
    v.tipo_de_contrato,
    v.ano,
    v.titulacao,
    v.experiencia,
    v.nacionalidade,
    v.lingua,
    v.area,
    GROUP_CONCAT(DISTINCT c.competencia) AS competencia,
    GROUP_CONCAT(DISTINCT r.requisitos) AS requisitos
FROM
    vagas as v
LEFT JOIN
    vaga_competencia as vc ON v.id = vc.id_vaga
LEFT JOIN
    competencia as c ON vc.id_competencia = c.id
LEFT JOIN
    vaga_requisitos as vr ON v.id = vr.id_vaga
LEFT JOIN
    requisitos as r ON vr.id_requisitos = r.id
GROUP BY
    v.id
```

> __SELECT__: Seleciona os campos que você deseja da tabela vagas e usa GROUP_CONCAT para concatenar as competências e aptidões em uma string separada por vírgulas.  
> __LEFT JOIN__: Usa LEFT JOIN para combinar as tabelas vagas, competencias, requisitos e as tabelas de associação vaga_competencia e vaga_requisitos. Isso garante que todas as vagas sejam retornadas mesmo se não houver competências ou aptidões associadas.  
> __GROUP BY__: Agrupa os resultados pela ID da vaga (v.id) para garantir que cada vaga apareça apenas uma vez no resultado final.

Segue-se abaixo a descrição de cada uma das colunas do nosso banco de dados:

- __Tabela `vagas`__

    1. __id__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador único da vaga. É a chave primária da tabela e é incrementado automaticamente.

    2. __cargo__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: O título ou nome do cargo da vaga de emprego. Por exemplo, "Técnica de Estrutura de TV".

    3. __setor__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: O setor ou indústria em que a vaga está inserida. Por exemplo, "Outros".

    4. __tipo_de_contrato__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: O tipo de contrato oferecido para a vaga. Por exemplo, "Tempo determinado".

    5. __ano__:
        - __Tipo__: `INT`
        - __Descrição__: O ano final de exibição da vaga. Deve ser uma data válida e não nula.

    6. __titulacao__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: O nível mínimo de educação ou titulação exigido para a vaga. Por exemplo, "Bacharelado".

    7. __experiencia__:
        - __Tipo__: `INT`
        - __Descrição__: A quantidade de experiência exigida para a vaga, em anos. Deve ser um valor inteiro e não nulo.

    8. __nacionalidade__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: A nacionalidade dos candidatos desejados. Por exemplo, "Angola".

    9. __lingua__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: As línguas exigidas ou preferidas para a vaga. Por exemplo, "Português".

    10. __area__:
        - __Tipo__: `VARCHAR(255)`
        - __Descrição__: A área funcional da vaga, que especifica o departamento ou função dentro da empresa. Por exemplo, "Técnica".

- __Tabela `competencias`__

    1. __id__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador único da competência. É a chave primária da tabela e é incrementado automaticamente.

    2. __competencia__:
        - __Tipo__: `TEXT`
        - __Descrição__: A descrição da competência exigida para a vaga. Por exemplo, "Configuração de equipamentos".

- __Tabela `vaga_competencia`__

    1. __id_vaga__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador da vaga. É uma chave estrangeira que faz referência à coluna `id` na tabela `vagas`.

    2. __id_competencia__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador da competência. É uma chave estrangeira que faz referência à coluna `id` na tabela `competencias`.

- __Tabela `requisitos`__
    1. __id__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador único da aptidão. É a chave primária da tabela e é incrementado automaticamente.

    2. __requisitos__:
        - __Tipo__: `TEXT`
        - __Descrição__: A descrição dos requisitos exigida para a vaga. Por exemplo, "Organização".

- __Tabela `vaga_requisitos`__

    1. __id_vaga__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador da vaga. É uma chave estrangeira que faz referência à coluna `id` na tabela `vagas`.

    2. __id_requisitos__:
        - __Tipo__: `INT`
        - __Descrição__: Identificador de requisitos. É uma chave estrangeira que faz referência à coluna `id` na tabela `requisitos`.

### __2.3 Qualidade dos Dados__

Para o projecto, se considerou o tamanho das __competencias__ e __requisitos__ como data type `varchar(255)`, diferente ao que condiz com o diagrama (O que é a forma certa). De tal modo que o  nosso conjunto de dados poderá ter algumas vagas que as __competencias__ e/ou os __requisitos__ não foram extraidos por conterem texto com caracteres superiores a 255.

## 3. Preparação dos Dados

- __Seleção de Dados__: Selecionar os dados relevantes para a análise.
- __Limpeza de Dados__: Limpar os dados para corrigir erros e inconsistências.
- __Transformação dos Dados__: Transformar os dados para o formato desejado.
- __Integração de Dados__: Integrar dados de diferentes fontes.
- __Formatação de Dados__: Formatar os dados para que possam ser usados por modelos de mineração.

## 4. Modelagem

- __Seleção de Técnicas de Modelagem__: Escolher os algoritmos e técnicas apropriadas.
- __Construção do Modelo__: Construir os modelos analíticos usando dados preparados.
- __Avaliação do Modelo*__: Avaliar a precisão e a validade dos modelos.

## 5. Avaliação

- __Avaliação dos Resultados__: Avaliar os modelos para garantir que eles atinjam os objetivos do negócio.
- __Revisão do Processo__: Revisar todo o processo de mineração de dados.
- __Próximos Passos__: Decidir os próximos passos com base nos resultados e na avaliação.

## 6. Implementação

- __Implementação do Modelo__: Implementar os modelos em um ambiente de produção.
- __Monitoramento e Manutenção__: Monitorar e manter os modelos para garantir que eles continuem a fornecer valor ao negócio.
