import scrapy
import json
import socket
import time
import nltk
nltk.download('punkt')

from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Classe para os itens raspado da página


class Itens(scrapy.Item):
    noticias = scrapy.Field()
    noticiasURL = scrapy.Field()


class SpiderNoticia(scrapy.Spider):
    name = 'Scraping noticias'

    def __init__(self, tag=None):
        url = "https://www.uol.com.br"
        self.start_urls = [url]
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.corpoNoticia = []

    def parse(self, response):

        HOST = '127.0.0.1'  
        PORT = 9999       

        stop_words = set(stopwords.words('portuguese'))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print('Conectado em:', addr)
                time.sleep(10)
                ################
                self.log('Lendo url: %s' % response.url)
                print('Lendo url: %s' % response.url)

                noticias = response.xpath(".//div[@class='headlineSub__content']")

                for noticia in noticias:
                    newLine = noticia.xpath(".//h3/text()")[0].get()

                    #removendo as stop worde a pontuação
                    tokenizer = nltk.RegexpTokenizer(r"\w+")                 
                    words = tokenizer.tokenize(newLine)
                    sentence_wo_stopwords = [word for word in words if not word in stop_words]

                    #enviado para o socket(streaming)
                    conn.sendall((unidecode(" ".join(sentence_wo_stopwords)).lstrip().rstrip()+ "\n").encode())


                    print("Enviando o titulo: ", newLine)
                    time.sleep(10)

        self.clientSocket.close()
                






