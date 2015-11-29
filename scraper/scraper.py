#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup;
import urllib, cStringIO,json, mechanize,re;
from PIL import Image;
from pymongo import MongoClient;
from time import gmtime, strftime
from urlparse import urlparse

class Scraper():
    def __init__(self,search):
        self.urls = [
            'http://memes.parawhatsapp.es/memes-de-viernes-para-whatsapp/'
        ];

        # Palabras a buscar
        self.search = search;

        # Array para obtener urls correctas
        self.urlsOpened = [];

        # Instanciamos pymongo
        self.client = MongoClient();
        # name db
        self.db = self.client.itsfriday;
        # name  collections
        self.collection = self.db.itsfriday;
        self.collection.drop();


    def checkUrls(self):
        for x in self.urls:
            try :
                urllib.urlopen(x);
                # Agregamos url
                self.urlsOpened.append(x);
            except IOError,e:
                print "Error en al abrir la url " + x;

        return self.urlsOpened;

    def parseHtml(self):
        for list in self.urlsOpened:
            url = urllib.urlopen(list).read();
            soup = BeautifulSoup(url,'lxml');

            # Buscar por a href o por img src
            i = 0;
            for images in soup.findAll('a'):
                if re.search("jpg",images['href']) or re.search("jpeg",images['href']) or re.search("png",images['href']):
                    #print images['href'];
                    file = cStringIO.StringIO(urllib.urlopen(images['href']).read())
                    im = Image.open(file);
                    width, height = im.size;

                    if width >= 300 and height >= 200:
                        #Insert Collection
                        self.setMemesInMongo(list, images['href']);


    # Funcion que inserta collection en mongo
    def setMemesInMongo(self, urlMeme, imageHref):
        self.collection.insert_one(
            {
                "img": imageHref,
                "name": imageHref,
                "source": urlMeme,
                "date_insert": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                "lang": "es"
            }
        );

    def printCollectionMongoIstFriday(self):
        cursor =  self.collection.find();
        for document in cursor:
            print(document)



    def getImagesGoogle(self):

        json_array_images_google = [];
        start = 0;
        end = 100

        search = self.search.replace(" ","%20");

        while start != 60:

            url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + str(search) + '&start=' + str(start));
            html = urllib.urlopen(url).read();

            json_objet = json.loads(html);

            print json_objet
            start+=1;






# Llamada ejemplo
search = "memes es viernes";
craw = Scraper(search);
"""
craw.checkUrls();
craw.parseHtml();
craw.printCollectionMongoIstFriday();
"""
craw.getImagesGoogle();
