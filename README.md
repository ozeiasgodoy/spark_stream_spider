# spark_stream_spider
Aplicação Streaming com Python e Spark para raspagem e contagem de palavras

# Requisitos
- Spark 
- Vs Code
- Python

# Bibliotecas
- Crie seu ambiente virtual e utilize o requirement.txt para instalar as bibliotexas necessárias

# Comandos
- Scraping
    scrapy runspider src/web_scraping.py
    
- Spark
    spark-submit --py-files src/count_word.py src/spark_app.py
