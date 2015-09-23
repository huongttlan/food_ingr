import simplejson as js
import json 
import dill
import itertools

import urllib2
from bs4 import BeautifulSoup
import re
import requests

#API key for bigoven.com
apiKey="h4RKPnV55591593Ty8gFjuw3tEqhGNDe"


f=open("search_df","r")
search_df=dill.load(f)
f.close()
#print search_df
print search_df.shape[0]

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
empty=[]
ingredients_all=[]
ingredients_name_all=[]
#Now need to crawl in ingredients in all IDs
# Cannot crawl every thing. Only 500 per one hour
for i in xrange(300,383):
    id= search_df.ix[i,'RecipeID']
    recipe_id="http://api.bigoven.com/recipe/"+id+"?api_key=" + apiKey
    #print recipe_id
    try:
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
        #ingredient_name=[x[1] for x in d if x[1][0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        ingredient_name=[x[1] for x in d]
        print ingredient_name
    
        #create a dictionary for ingredient
        #ingredient= dict(itertools.izip(ingredient_id,ingredient_name))
    
        #Now add in the whole list
        #ingredients_all.append(ingredient)
        ingredients_name_all.append(ingredient_name)
    except:
        print recipe_id
        ingredients_name_all.append(empty)

    
#print len(ingredients_name_all)
#print len(ingredients_all)
print ingredients_name_all
'''
f=open("ingredients_name_all_100","wb")
dill.dump(ingredients_name_all, f)
f.close()
'''
'''
f=open("ingredients_name_all_200","wb")
dill.dump(ingredients_name_all, f)
f.close()
'''
'''
f=open("ingredients_name_all_300","wb")
dill.dump(ingredients_name_all, f)
f.close()
'''
f=open("ingredients_name_all_383","wb")
dill.dump(ingredients_name_all, f)
f.close()







'''
#Total Minutes

#totalminutes=[float(x.contents[0]) for x in values_id.find_all('totalminutes')][0]

#Active Minutes
#activeminutes=[float(x.contents[0]) for x in values_id.find_all('activeminutes')][0]
''' 