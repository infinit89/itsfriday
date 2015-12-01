#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,json;
from pymongo import MongoClient;
from time import gmtime, strftime

class Scraper():
    def __init__(self,search, lang):

        #Words to search
        self.search = search;

        #Language
        self.lang = lang;

        #Instance pymongo
        self.client = MongoClient();

        #Name DB
        self.db = self.client.itsfriday;

        #Name Collections
        self.collection = self.db.itsfriday;

    #Set images in MongoDB
    def setMemesInMongo(self,title ,urlImage ,sourceUrlImage):

        searchImage = self.collection.find_one({"urlImage": urlImage});

        if searchImage == None:
            self.collection.insert_one(
                {
                    "urlImage": urlImage,
                    "title": title,
                    "source": sourceUrlImage,
                    "date_insert": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                    "lang": self.lang
                }
            );

    def printCollectionMongo(self):
        cursor = self.collection.find();
        for document in cursor:
            print(document)


    def getImagesGoogle(self):

        cont = 10;

        #If txt file contains a number for startIndex
        if self.loadStartIndex() != "":
            start = int(self.loadStartIndex());
            end = (int(self.loadStartIndex()) + cont);

            search = self.search.replace(" ","%20");

            while start != end:

                url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + str(search) + '&start=' + str(start));
                html = urllib.urlopen(url).read();

                json_objet = json.loads(html);

                if str(json_objet['responseData']) not in "None":
                    for results in json_objet['responseData']['results']:
                        titleNoFormatting = results['titleNoFormatting']; #title without html
                        sourceUrlImage = results['originalContextUrl']; #url source
                        width = results['width'];
                        height = results['height'];
                        url = results['url'];

                        #More data
                        #unescapedUrl = results['unescapedUrl'];
                        #title = results['title']; #title with html
                        #imageId = results['imageId'];


                        if width >= 300 and height >= 200:
                            #Inserta data
                            self.setMemesInMongo(titleNoFormatting,url,sourceUrlImage);
                start+=1;

            end = start;
            self.setNewStartIndex(end);
        else:
            #error
            print "Ups , an error has occurred in txt file"

    #Load current startIndex from txt file
    def loadStartIndex(self):
        f = open('./txt/startIndex.txt','r')
        index = ""

        while 1:
            line = f.readline()
            if not line:break
            index += line

        f.close()

        return index

    #Set new startIndex into txt file
    def setNewStartIndex(self,index):
        f = open('./txt/startIndex.txt','w');

        #Delete content
        f.truncate();
        #Write new startIndex
        f.write(str(index));

        f.close();


#Example
search = "memes es viernes";

# New instance
scraper = Scraper(search, 'es');

scraper.getImagesGoogle();
scraper.printCollectionMongo();
