# __ANALISE EM VAGAS DE EMPREGO__

![The photo was taken from THE DREADED JOB SEARCH and inc.com](/imgs/job_search.png)
[fonte: Job Market Analysis](https://medium.com/sfu-cspmp/job-market-analysis-a905b9a29a31)

## 1. Entendimento do Negócio

O mercado de trabalho é muito competitivo e complicado, especialmente para aqueles que estão fora do mercado de trabalho, ou para quem pretende fazer uma transição.
Sendo que os recrutadores pedem vários requisitos em uma vaga de trabalho, entre eles anos de experiências, formação, habilidades e certificações, saber quais são os requisitos mais frequentemente pedidos para uma categoria ou área, poderia ajudar aqueles fora do mercado laboral, a se prepararem melhor quando forem a se preparar para uma dada vaga.

### __1.1 - Objetivos do Negócio__

Identificar os requisitos importantes que os recrutadores pedem para uma vaga de trabalho de determinada área.

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

> **SELECT**: Seleciona os campos que você deseja da tabela vagas e usa GROUP_CONCAT para concatenar as competências e aptidões em uma string separada por vírgulas.  
> **LEFT JOIN**: Usa LEFT JOIN para combinar as tabelas vagas, competencias, requisitos e as tabelas de associação vaga_competencia e vaga_requisitos. Isso garante que todas as vagas sejam retornadas mesmo se não houver competências ou aptidões associadas.  
> **GROUP BY**: Agrupa os resultados pela ID da vaga (v.id) para garantir que cada vaga apareça apenas uma vez no resultado final.

### __2.3 Qualidade dos Dados__

Verificar a qualidade e integridade dos dados.

## 3. Preparação dos Dados

   - **Seleção de Dados**: Selecionar os dados relevantes para a análise.
   - **Limpeza de Dados**: Limpar os dados para corrigir erros e inconsistências.
   - **Transformação dos Dados**: Transformar os dados para o formato desejado.
   - **Integração de Dados**: Integrar dados de diferentes fontes.
   - **Formatação de Dados**: Formatar os dados para que possam ser usados por modelos de mineração.

## 4. Modelagem

   - **Seleção de Técnicas de Modelagem**: Escolher os algoritmos e técnicas apropriadas.
   - **Construção do Modelo**: Construir os modelos analíticos usando dados preparados.
   - **Avaliação do Modelo**: Avaliar a precisão e a validade dos modelos.

## 5. Avaliação

   - **Avaliação dos Resultados**: Avaliar os modelos para garantir que eles atinjam os objetivos do negócio.
   - **Revisão do Processo**: Revisar todo o processo de mineração de dados.
   - **Próximos Passos**: Decidir os próximos passos com base nos resultados e na avaliação.

## 6. Implementação

   - **Implementação do Modelo**: Implementar os modelos em um ambiente de produção.
   - **Monitoramento e Manutenção**: Monitorar e manter os modelos para garantir que eles continuem a fornecer valor ao negócio.

