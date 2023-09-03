# NOTES FOR THE DEVELOPER:
# Update API_KEY and ORG_ID values for your organization. They can be extracted from:
#       ORG_ID  => https://beta.openai.com/account/org-settings
#       API_KEY => https://beta.openai.com/account/api-keys
# to customize product keywords: change "product_keywords" list
# to customize blog's content length: increase/decrease "max_tokens" variable however it has a max quota
# changing the "temperature" parameter from 0 to 1 allows you to adjust the degree of "creativity" of the model
# to customize generated image sizes: modify "size" value in "image_response" request parameters.
# AI Image size value must be one of 256x256, 512x512, or 1024x1024

import json
import openai
import sqlite3
import pymysql
import configparser
import pandas
import requests

config = configparser.ConfigParser()
config.read('config.ini')

host = config['DATABASE OUTPUT']['host']
name = config['DATABASE OUTPUT']['name']
password = config['DATABASE OUTPUT']['password']
database = config['DATABASE OUTPUT']['database']
table_name = config['DATABASE OUTPUT']['table_name']
file = pandas.read_excel(config['FILE PATH']['file_name']).values.tolist()


con = pymysql.connect(host,name,password,database)
#openai.organization = config['SETTINGS']['ORG_ID']
openai.api_key = config['SETTINGS']['API_KEY']
openai.Model.list()

blogs_dictionary = []

# the following products list is highly customizable
cur = con.cursor()
# Create table if not exist
cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER NOT NULL PRIMARY KEY,
                blog_title TEXT,
                blog_content TEXT,
                blog_image TEXT);""")
for row in file:
    temperat = row[3]
    max_lenth = row[2]
    what_need = row[1]
    image_enable = int(row[3])
    product_keywords = [x for x in row[0].split(',')]
    for prompt in product_keywords:
        # Create AI generated Blog from prompt
        blog_response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"{what_need} {prompt.strip()}",
            max_tokens=int(max_lenth),
            temperature=int(temperat),
        )
        blog_content = blog_response["choices"][0]["text"].strip()

        # Create AI generated image from prompt
        image_url = None
        if image_enable == 1:
            image_response = openai.Image.create(
                prompt=f"A {prompt}",
                n=1,
                size="256x256"
            )
            image_url = image_response["data"][0]["url"]
            with open('prompt.strip().jpeg','wb') as f:
                f.write(requests.get(image_url).content)
        blogs_dictionary.append({
            'blog_title': prompt.strip(),
            'blog_content': blog_content.strip(),
            'blog_image': image_url,
             'task':what_need
        })

        cur.execute(f"""INSERT INTO {table_name} (blog_title,blog_content,blog_image) VALUES (?,?,?);""",(prompt.strip(),blog_content.strip(),image_url))
        con.commit()
    pandas.DataFrame(blogs_dictionary).to_excel('OpenAI.xlsx')
con.close()

