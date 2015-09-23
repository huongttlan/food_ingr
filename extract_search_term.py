import pandas as pd
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

import urllib2
from bs4 import BeautifulSoup
import re
import requests

import nltk
from datetime import datetime

import simplejson as js
import json 
import dill
import itertools

#API key for bigoven.com
apiKey="h4RKPnV55591593Ty8gFjuw3tEqhGNDe"

#This is an example of how to download the Italian chicken term search
titleKeyword="Italian chicken"
#Need to transform the blank space into %20
titleKeyword=titleKeyword.replace (" ", "%20")
pgno=1
search_term="http://api.bigoven.com/recipes?pg=" + str(pgno) + "&rpp=200&title_kw="\
            + titleKeyword + "&api_key=" + apiKey
print search_term  

req_search = urllib2.Request(search_term)
response_search = urllib2.urlopen(req_search)
page_search = response_search.read()
values_search=BeautifulSoup(page_search,"html.parser")
#print values_search.prettify()

#Crawl first in order to get the number of results count
results_count=int(values_search.find('resultcount').contents[0])
#print results_count

recipe_id=[]    #For recipe id
recipe_title=[]  #For title
recipe_rating=[] #For star ratings
recipe_cuisine=[] #For cuisine
recipe_url=[] #For url


recipe_id=recipe_id + [str(x.contents[0]) for x in values_search.find_all('recipeid')]
recipe_rating=recipe_rating + [float(x.contents[0]) for x in values_search.find_all('starrating')]
recipe_title=recipe_title + [unicode(x.contents[0]) for x in values_search.find_all('title')]

cuis=values_search.find_all('recipeinfo')
for x in cuis:
    a=re.search(r'<cuisine>',unicode(x))
    b=re.search(r'</cuisine>',unicode(x))
    
    if a and b:
        recipe_cuisine.append(unicode(x)[a.end():b.start()])
    else:
        recipe_cuisine.append("")
        
#recipe_cuisine=recipe_cuisine + [unicode(x.contents[0]) for x in values_search.find_all('cuisine')]
#print recipe_cuisine

recipe_url=recipe_url + [unicode(x.contents[0]) for x in values_search.find_all('imageurl')]

while len(recipe_id) <results_count:
    pgno+=1
    search_term="http://api.bigoven.com/recipes?pg=" + str(pgno) + "&rpp=200&title_kw="\
            + titleKeyword + "&api_key=" + apiKey
    req_search = urllib2.Request(search_term)
    response_search = urllib2.urlopen(req_search)
    page_search = response_search.read()
    values_search=BeautifulSoup(page_search,"html.parser")
    
    recipe_id=recipe_id + [str(x.contents[0]) for x in values_search.find_all('recipeid')]
    recipe_rating=recipe_rating + [float(x.contents[0]) for x in values_search.find_all('starrating')]
    recipe_title=recipe_title + [unicode(x.contents[0]) for x in values_search.find_all('title')]
    cuis=values_search.find_all('recipeinfo')
    for x in cuis:
        a=re.search(r'<cuisine>',unicode(x))
        b=re.search(r'</cuisine>',unicode(x))
        if a and b:
            recipe_cuisine.append(unicode(x)[a.end():b.start()])
        else:
            recipe_cuisine.append("")
    recipe_url=recipe_url + [unicode(x.contents[0]) for x in values_search.find_all('imageurl')]


search_df=pd.DataFrame({'RecipeID':recipe_id, 'ReciptTitle':recipe_title, 'RecipeRating':recipe_rating,\
                'RecipeCuisine':recipe_cuisine,'RecipeUrl':recipe_url})

f=open("search_df","wb")
dill.dump(search_df, f)
f.close()

################################################
#Ok, now extract the list of ingredients
'''
for i in recipe_id:
    recipe_id="http://api.bigoven.com/recipe/"+i+"?api_key=" + apiKey
    req_id = urllib2.Request(recipe_id)
    response_id = urllib2.urlopen(req_id)
    page_id = response_id.read()
    values_id=BeautifulSoup(page_id,"html.parser")
'''    

#Now need to crawl in ingredients in all IDs




#This is the example of the recipe crawling
recipe_id="http://api.bigoven.com/recipe/"+"201809"+"?api_key=" + apiKey
print recipe_id
req_id = urllib2.Request(recipe_id)
response_id = urllib2.urlopen(req_id)
page_id = response_id.read()
values_id=BeautifulSoup(page_id,"html.parser")

ingredient_list=values_id.find_all('ingredients')
#print ingredient_list

#ingredient id
c=re.findall(r'(<ingredientid>)(\w*)(</ingredientid>)',unicode(ingredient_list))
ingredient_id=[x[1] for x in c]

#ingredient name
d=re.findall(r'(<name>)((w*\s*\w*)*)(</name>)',unicode(ingredient_list))
ingredient_name=[x[1] for x in d if x[1][0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

#create a dictionary for ingredient
ingredient= dict(itertools.izip(ingredient_id,ingredient_name))
print ingredient

#ingredient_HTML

#Total Minutes

totalminutes=[float(x.contents[0]) for x in values_id.find_all('totalminutes')][0]

#Active Minutes
activeminutes=[float(x.contents[0]) for x in values_id.find_all('activeminutes')][0]









              
#####################
#Another way
'''
import httplib2 as http
import json

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

target=urlparse(search_term)
method = 'GET'
body = ''

h = http.Http()
response, content = h.request(target.geturl(), method, body, headers)
data = json.loads(content)
#print len(data['Results'])
'''
#####################

