#!/usr/bin/python3
# importing necessary packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import os
import time
import requests
import re
from urllib.request import urlretrieve
# import json
# from pandas.io.json import json_normalize
# import pandas as pd, numpy as np


# Taking username 
URL = "https://www.instagram.com/"
ID = input("Enter username : ")
N = input("Number of posts (0 for all) : ")
if N == "0":
	N = 99999999
else :
	N = int(N)

# launching the firefox browser with instagram's URL
print("Loading browser and opening page :")
driver = webdriver.Firefox()
driver.get(URL + ID)
if "Page Not Found" in driver.title:
	print(driver.title)
	exit(0)
print(driver.title)
pg_size = driver.execute_script("return document.body.scrollHeight;")

pg_size2 = 0
imagesSet = set()

# Scrolling page till end of page and storing Image tags of posts in set
for i in range(200):
    page = driver.page_source
    soup = bs(page,'html.parser')
    images = soup.findAll('img',attrs={'class': 'FFVAD'})
    imagesSet = imagesSet.union(images)
    
    print("\rPlease wait while we Scroll Pages. {} images found.".format(len(imagesSet)),end="")

    # ending search if given number of image found
    if len(imagesSet) > int(N):
        print("{} image Search completed.".format(N))
        break

    #ending search if any error occurs
    try:
    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e :
        print("Error occured while looking for more images :", str(e))
        break

    time.sleep(5)
    pg_size2 = driver.execute_script("return document.body.scrollHeight;")

    #ending search if unable to load more images
    if pg_size2 == pg_size:
        time.sleep(10)
        pg_size2 = driver.execute_script("return document.body.scrollHeight;")
        if pg_size2 == pg_size:
            print("No more image available")
            break
    else:
        pg_size = pg_size2

driver.close()


# Extracting Caption and URL of image posts
img_urls = []
for image in imagesSet:
    if 'alt' in image.attrs and 'src' in image.attrs:
        img_urls.append([image['alt'],image['src'] ])
    elif 'src' in image.attrs:
    	img_urls.append(["no caption",image['src'] ])


if not os.path.exists("./DownloadedImages/"+ID):
    os.makedirs("./DownloadedImages/"+ID)
# len(img_urls)


# downloading all Images post from list
countSuccess = 0
countFailed = 0
for urls in img_urls:
    img_src = urlparse(urls[1])
    filename = os.path.basename(img_src.path)
    try:
        urlretrieve(urls[1], "./DownloadedImages/"+ID+"/" + filename)
        countSuccess = countSuccess+1
        print("{}/{} : {} downloaded.".format(countSuccess,len(img_urls),filename ))
    except Exception as e:
        print(filename," - failed to download ",str(e))
        countFailed = countFailed + 1
print("{} Sucessfully downloaded, {} Failed Out of {}".format(countSuccess,countFailed, len(img_urls)  ))

# Storing the caption of images
with open( "./DownloadedImages/"+ID+"/" +"image_info.txt",'w') as f:
    for urls in img_urls:
        img_src = urlparse(urls[1])
        filename = os.path.basename(img_src.path)
        f.write(" >>>> " + filename  )
        f.write("\n"+"-"*57+ "\n")
        f.write(urls[0])
        f.write("\n\n"+"-"*120+ "\n\n")

# Storing analyzed pic data
tags = {}
for urls in img_urls:
    if "Image may contain" in urls[0]:
        img_src = urlparse(urls[1])
        filename = os.path.basename(img_src.path)
        a = re.split('Image may contain: |, | and ',urls[0])
        tags[filename] = a[1:]
        
with open("./DownloadedImages/"+ID+"/" +"Metadata.txt",'w') as f:
    f.write(str(tags))
    

# if __name__ == '__main__':
# 	main()

