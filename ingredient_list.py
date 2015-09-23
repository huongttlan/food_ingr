import simplejson as js
import json 
import dill
import itertools

import urllib2
from bs4 import BeautifulSoup
import re
import requests

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


f=open("search_df","r")
search_df=dill.load(f)
f.close()
#print search_df


#Extract the 
f=open("ingredients_name_all_100","r")
ingredients_name_all_100=dill.load(f)
f.close()

f=open("ingredients_name_all_200","r")
ingredients_name_all_200=dill.load(f)
f.close()

f=open("ingredients_name_all_300","r")
ingredients_name_all_300=dill.load(f)
f.close()

f=open("ingredients_name_all_383","r")
ingredients_name_all_383=dill.load(f)
f.close()


ingredients_name=ingredients_name_all_100+ ingredients_name_all_200 + \
                ingredients_name_all_300 + ingredients_name_all_383


search_df['Ingredients']=ingredients_name

#to lower case the ingredients:
for i in xrange(0, search_df.shape[0]):  
    search_df['Ingredients'].values[i]=[x.lower() for x in search_df['Ingredients'].values[i]]
#print search_df


#Now remove those that have no pictures
for x in xrange(0, search_df.shape[0]):
    if search_df.ix[x,'RecipeUrl'].find('recipe-no-image')==-1:
        search_df.ix[x,'Imgchk']=False
    else:
        search_df.ix[x,'Imgchk']=True
        search_df1=search_df[search_df['Imgchk']==False]
search_df1.is_copy=False
#print search_df1

#Now remove those that have the rating <3
search_df2=search_df1[search_df1['RecipeRating']>=3]
search_df2.is_copy=False
print search_df2


#Now we need to remove, for example, chili flakes
Ingrchk=[]
for x in xrange(0, search_df2.shape[0]):
    temp=False
    for j in search_df2['Ingredients'].values[x]:
        if j.find('chili flake')!=-1:
            temp=True
    Ingrchk.append(temp)
    
search_df2['Ingrchk']=Ingrchk
find_df=search_df2[search_df2['Ingrchk']==True]
find_df.is_copy=False
#print find_df

search_df3=search_df2[search_df2['Ingrchk']==False]
search_df3.is_copy=False


#Ok, now work with set of ingredients
ingredient_set=set()
ingredient_dict={}



for i in xrange(0, search_df.shape[0]):  
    #search_df1['Ingredients'].values[i]=[x.lower() for x in search_df1['Ingredients'].values[i]]  
    temp=set(search_df.ix[i,'Ingredients'])

    for j in temp:
        chk = ingredient_dict.get(j)
        if chk is not None:
            ingredient_dict[j]+=1
        else:
            ingredient_dict[j]=1

#print ingredient_dict
from matplotlib import pyplot as plt

ingredient_df=pd.DataFrame({'ingredient_name' : ingredient_dict.keys() ,\
                            'count' : ingredient_dict.values()}).sort('count',ascending=False)

#ingredient_df

ingredient_df_sub=ingredient_df[:20]

print ingredient_df_sub

