


from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
# este scrapy de la pagina de la loteria esta echo con la libreria scrapy 
# por asuntos de tiempo lo puse a guardar en un achivo de excel pero seria la misma logica si se guardara en una base de datos mongoose o mysql ect
class Loteria(Item):
    id = Field()
    numero = Field()

# CLASE CORE - SPIDER
class LoteriaSpider(Spider):
    name = "SpiderLoteria" # nombre, puede ser cualquiera 
    
    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }    

    # URL SEMILLA
    start_urls = ['https://www.conectate.com.do/loterias/nacional']


    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla
    def parse(self, response):
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response) 
        titulo_de_pagina = sel.xpath('//a/text()').get()
        print (titulo_de_pagina)
        # Selector de varias div
        preguntas = sel.xpath('//div[@class="game-block past"]//div[@class="game-scores ball-mode"]') 
        # yield preguntas.load_item()
        i = 0
        for pregunta in preguntas:
            item = ItemLoader(Loteria(), pregunta) # Instancio mi ITEM con el selector en donde estan los datos para llenarlo

            # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector 
            item.add_xpath('numero', './/span/text()')
            item.add_value('id', i)
            i += 1
            yield item.load_item() # Hago Yield de la informacion para que se escriban los datos en el archivo

# EJECUCION EN TERMINAL:
# scrapy runspider _scrapy_loteria.py -o resultados.csv -t csv