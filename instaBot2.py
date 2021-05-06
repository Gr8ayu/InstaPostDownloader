import concurrent.futures
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import os
import time
import requests
import re
from sys import exit
from getpass import getpass
from urllib.request import urlretrieve

class colorPrint:

	colors = {
	'W'  : '\033[0m'  ,# white (normal)
	'R'  : '\033[31m' ,# red
	'G'  : '\033[32m' ,# green
	'O'  : '\033[33m' ,# orange
	'B'  : '\033[34m' ,# blue
	'P'  : '\033[35m' ,# purple
	}
	text = ""

	def __init__(self, text,start):
		if start in self.colors.keys() :
			self.text = self.colors[start] + text + self.colors['W']
# 			print(self.colors[start] + text + self.colors['W'] )
		else:
			self.text = text 
	def print(self,end="\n"):
		print(self.text,end=end)

class instabot:

	URL = "https://www.instagram.com/"
	
	# username of target
	ID = "" 


	# stores image Tags in html format
	imagesSet = set()

	# stores image IDs
	tagsSet = set()
	tagsSetSuccess = set()
	tagsSetFailed = set()

	# stores url of image in HD resolution
	original_img_URLs = []
	original_img_URLsSuccess = []
	original_img_URLsFailed = []

	# stores 640x640p image url with caption
	img_urls = []
	img_urlsSuccess = []
	img_urlsFailed = []

	# stores the no of image to download
	N = 100

	# username and password of host
	user = ""
	passwd = ""
	
	isprivate = False


	def __init__(self, id):
		self.ID = id
		

	def login(self,driver):
		# self.user = input("Enter your username :")
		# self.passwd = getpass("Password : ")
		
		try:
			
			driver.get(self.URL +"accounts/login/?next=%2F"+ self.ID)
			if "Continue as" in driver.page_source:
				element = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/div[2]/button")
				element.click()
			
			#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')))
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))).send_keys(self.user)
			# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Password']"))).send_keys(self.passwd)
			# user_input = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
			# user_pass = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input"))).send_keys(self.passwd)
			
			# user_input.send_keys(self.user)
			#user_pass.send_keys(self.passwd)

			#submit = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button").click()
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".L3NKy"))).click()
			

			time.sleep(self.sleep_time)
		except Exception as e:
			colorPrint("Error occured. Try Again." + str(e),'R').print()
			return False 
		else:
			if self.ID in driver.title:
				colorPrint("Logged In.",'G').print()
				return True
			else:
				colorPrint("LogIn failed. Try Again.",'R').print()
				return False


	def getData(self):
		# launching the firefox browser with instagram's URL
		start = time.time()
		print("Loading browser and opening page :")
		
		profile = webdriver.FirefoxProfile()
		profile.set_preference('permissions.default.image',2)
		driver = webdriver.Firefox(firefox_profile = profile)
		try:
			driver.get(self.URL + self.ID)
		except Exception as e:
			colorPrint("Error occured. Try Again.",'R').print()
		else:
			pass
		finally:
			pass

		if "This Account is Private" in driver.page_source:
			self.isprivate = True
			loginStatus = False
			while not loginStatus:
				loginStatus = self.login(driver)

			# https://www.instagram.com/accounts/login/?next=%2Frizafareed
			# https://www.instagram.com/accounts/login/?next=%2Fayu_gr8
		if "Page Not Found" in driver.title:
			print(driver.title)
			exit(0)
		colorPrint(driver.title,'P').print()
		pg_size = driver.execute_script("return document.body.scrollHeight;")
		pg_size2 = 0

		# Scrolling page till end of page and storing Image tags of posts in set
		for i in range(200):
			page = driver.page_source
			soup = bs(page,'html.parser')
			
			images = soup.findAll('img',attrs={'class': 'FFVAD'})
			imagesTag = soup.findAll('div',attrs={'class': 'v1Nh3'})

			tags = [imageTag.find('a').attrs['href'] for imageTag in imagesTag ]
			
			self.tagsSet = self.tagsSet.union(tags)
			self.imagesSet = self.imagesSet.union(images)
			
			print("\rPlease wait while we Scroll Pages. {} images found.".format(len(self.imagesSet)),end="")

			# ending search if given number of image found
			if len(self.imagesSet) > int(self.N):
				print()
				colorPrint("{} image Search completed.".format(self.N),'G').print()
				
				break

			#ending search if any error occurs
			try:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			except Exception as e :
				
				colorPrint("Error occured while looking for more images :"+ str(e),'R').print()

				break

			time.sleep(self.sleep_time)
			pg_size2 = driver.execute_script("return document.body.scrollHeight;")

			#ending search if unable to load more images
			if pg_size2 == pg_size:
				time.sleep(2*self.sleep_time)
				pg_size2 = driver.execute_script("return document.body.scrollHeight;")
				if pg_size2 == pg_size:
					colorPrint("No more image available",'G').print()
					break
			else:
				pg_size = pg_size2

		driver.close()
		end = time.time()
		hours, rem = divmod(end-start, 3600)
		minutes, seconds = divmod(rem, 60)
		print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


	def configure(self):
		self.ID = input("Enter username : ")
		self.N = input("Number of posts (0 for all) : ")
		self.user = input("Enter your username :")
		self.passwd = getpass("Password : ")
		
		if self.N == "0":
			self.N = 99999999
		else :
			self.N = int(self.N)
		self.sleep_time = int(input("seconds to timeout :")) 


	def getURLs(self):
		self.img_urls = []
		for image in self.imagesSet :
			if 'alt' in image.attrs and 'src' in image.attrs:
				self.img_urls.append({'alt':image['alt'], 'src':image['src'] })
			
			elif 'src' in image.attrs:
				self.img_urls.append({'alt':'no caption', 'src':image['src'] })

	def get_original_img_URLs(self,tags):
		start = time.time()
		self.original_img_URLs = []
		print("\rExtracting original Image url : ")

		if self.isprivate == True:
			profile = webdriver.FirefoxProfile()
			profile.set_preference('permissions.default.image',2)
			driver = webdriver.Firefox(firefox_profile = profile)
		
			loginStatus,count = False,0
			while not loginStatus and count!=10:

				loginStatus = self.login(driver)
				count +=1

		for tag in tags :
			url = 'https://www.instagram.com' + tag
			
			if self.isprivate:
				try:
					driver.get(url)
					page = driver.page_source
					
					soup = bs(page,'html.parser')
					
					self.original_img_URLs.append(soup.find('img',attrs={'class': 'FFVAD'})['src'])
					self.tagsSetSuccess.add(tag)

				except Exception as e:
					self.tagsSetFailed.add(tag)
					colorPrint(str(e),'R').print()



			else:
				try:
					response = requests.get(url)
					page = response.content
				except Exception as e:
					colorPrint(str(e),'R').print()
					continue
			
				soup = bs(page,'html.parser')
				try:
					self.original_img_URLs.append(soup.find('meta',attrs={'property': 'og:image'})['content'])
					self.tagsSetSuccess.add(tag)
				except Exception as e:
					self.tagsSetFailed.add(tag)
					colorPrint(str(e),'R').print()
			

			colorPrint("\r [{}|{} complete]".format(len(self.original_img_URLs),len(self.tagsSet)),'O').print(end="") 
		print("")
		end = time.time()
		hours, rem = divmod(end-start, 3600)
		minutes, seconds = divmod(rem, 60)
		print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
		#driver.close()
		  

	def downloadImages(self,URLs):
		if not os.path.exists("./DownloadedImages/"+ID):
			os.makedirs("./DownloadedImages/"+ID)

		countSuccess = 0
		countFailed = 0
		for urls in URLs:
			img_src = urlparse(urls['src'])
			filename = os.path.basename(img_src.path)
			try:
				urlretrieve(urls[1], "./DownloadedImages/"+ID+"/" + filename)
				countSuccess = countSuccess+1
				#print("{}/{} : {} downloaded.".format(countSuccess,len(URLs),filename ))
			except Exception as e:
				print(filename," - failed to download ",str(e))
				countFailed = countFailed + 1
		print("\r{} Sucessfully downloaded, {} Failed Out of {}  ".format(countSuccess,countFailed, len(URLs)  ))


	def downloadFile(self, url):
		# filename = os.path.basename(url)
		filename = os.path.basename(urlparse(url).path)
		try:
			urlretrieve(url, "./DownloadedImages/"+self.ID+"/" + filename)
			#print("{}/{} : {} downloaded.".format(countSuccess,len(URLs),filename ))
			# colorPrint(filename + "downloaded.",'G').print()
			self.original_img_URLsSuccess.append(url)
			if url in self.original_img_URLsFailed:
				original_img_URLsFailed.remove(url)
			return True

		except Exception as e:
			print(filename," - failed to download ",str(e))
			# countFailed = countFailed + 1
			self.original_img_URLsFailed.append(url)
			if url in self.original_img_URLsSuccess:
				original_img_URLsSuccess.remove(url)
			return False



	def downloadThreaded(self,URLs):
		start   = time.time()
		if not os.path.exists("./DownloadedImages/"+self.ID):
			os.makedirs("./DownloadedImages/"+self.ID)
		countSuccess = 0
		countFailed = 0
		results = []
		print("Downloading Images : ")
		with concurrent.futures.ThreadPoolExecutor() as executor:
			for url in URLs:
				results.append(executor.submit(self.downloadFile,url)  )
			for f in concurrent.futures.as_completed(results):
				if f.result() == True :
					countSuccess += 1
					# self.original_img_URLsSuccess.append(url)
				else :
					countFailed += 1
					# self.original_img_URLsFailed.append(url)
				
				colorPrint("\rSuccess : {} | Failed : {} | Total : {}  ".format(countSuccess,countFailed, len(URLs)) ,'P').print(end="")
			print("")
			end = time.time()
			hours, rem = divmod(end-start, 3600)
			minutes, seconds = divmod(rem, 60)
			print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

	def start(self):
		self.configure()
		self.getData()
		self.get_original_img_URLs(self.tagsSet)
		self.downloadThreaded(self.original_img_URLs)
		self.writeJson()

	def writeJson(self):
		data = {
			'ID' : self.ID,
			
			'tagsSet' : list(self.tagsSet),
			'tagsSetSuccess' : list(self.tagsSetSuccess),
			'tagsSetFailed' : list(self.tagsSetFailed),
			
			'original_img_URLs' : self.original_img_URLs,
			'original_img_URLsSuccess' : self.original_img_URLsSuccess,
			'original_img_URLsFailed' : self.original_img_URLsFailed,
			
			'img_urls' : self.img_urls,
			'img_urlsSuccess' : self.img_urlsSuccess,
			'img_urlsFailed' : self.img_urlsFailed,
			
			'isprivate' : self.isprivate
		}

		json_data = json.dumps(data, indent=4)

		#     print(json_data)
		if not os.path.exists("./DownloadedImages/"+self.ID):
			os.makedirs("./DownloadedImages/"+self.ID)
		with open("./DownloadedImages/"+self.ID + '/data.json', 'w') as the_file:
			the_file.write(json_data)


	def readJson(self):
		with open("./DownloadedImages/"+self.ID + '/data.json') as json_data:
			d = json.load(json_data)
			json_data.close()
			return d



if __name__ == '__main__':
	
	help_text = """
	bot = instabot("")
	bot.configure()
	bot.getData()
	bot.get_original_img_URLs(bot.tagsSet)
	bot.downloadThreaded(bot.original_img_URLs)
	bot.writeJson()
	"""
	print(help_text)

	bot = instabot("")
	bot.configure()
	bot.getData()
	bot.get_original_img_URLs(bot.tagsSet)
	bot.downloadThreaded(bot.original_img_URLs)
	bot.writeJson()







"""
<video class="tWeCl" playsinline="" poster="https://instagram.fblr1-3.fna.fbcdn.net/vp/022398d0a16846dae5c8914c66282a15/5DBAE65F/t51.2885-15/e35/70697535_144677046908516_3312049126137235514_n.jpg?_nc_ht=instagram.fblr1-3.fna.fbcdn.net&amp;_nc_cat=1" preload="none" type="video/mp4" src="https://instagram.fblr1-3.fna.fbcdn.net/v/t50.2886-16/74757683_1247474635454799_7875974191320504909_n.mp4?_nc_ht=instagram.fblr1-3.fna.fbcdn.net&amp;_nc_cat=103&amp;oe=5DBA93EB&amp;oh=1580cee9857d97a756f87d498b76ad02"></video>

"""
