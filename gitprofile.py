import csv
import requests
import urllib.request
import os
from PIL import Image

#Proportionately resizes the logo as per this factor
resize_factor = 0.15
os.makedirs('withlogo', exist_ok = True)

with open('input.csv', 'r') as read_obj:
	csv_reader = csv.reader(read_obj)
	usernames = list(csv_reader)[0]

def add_logo(im):
	logo_file = 'logo.png'
	logoIm = Image.open(logo_file).convert('RGBA')
	
	width, height = im.size
	logoIm = logoIm.resize((int(resize_factor*width), int(resize_factor*height)))
	logoWidth, logoHeight = logoIm.size
	im.paste(logoIm, (width-logoWidth-10, height-logoHeight-10), logoIm)
	return im

for user in usernames:

	url='https://api.github.com/users/'+user
	r = requests.get(url)
	data=r.json()
	img_url= data.get('avatar_url')

	print(img_url)

	img = Image.open(requests.get(img_url, stream=True).raw)

	img_withlogo = add_logo(img)

	img_withlogo.save(os.path.join('withlogo', user+'.jpeg'))
