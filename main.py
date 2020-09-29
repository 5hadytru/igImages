from PIL import Image, ImageDraw, ImageOps, ImageFont
import requests as r
from bs4 import BeautifulSoup as bs
import os
import string
import math
import random
from captions import author, quote
import textwrap

# Scrape image from db and write to folder
def write_image_to_folder():

    links = []
    dump_path = "D:/thick/Git/Bots/instaBot/igManager/images/honua1/image"
    url = "https://unsplash.com/s/photos/" + "iceland" # finish getting images -> overlay and paste -> save -> test and complete bot

    req = r.get(url)

    if req.status_code < 300 and req.status_code >= 200 :
        soup = bs(req.text, 'lxml')  # returns parsed source code
        all_with_title = soup.find_all('a', attrs={'title': 'Download photo'})
        for i in all_with_title:
            links.append(i['href'])

    else:
        print("Status code error (website inaccessible)\n")
    
    counter = 60 ######################################################

    if len(links) > 0:
        for dl_link in links:
            img = r.get(dl_link)
            with open(dump_path + str(counter) + '.jpg', 'wb') as f:
                f.write(img.content)
            pilImg = Image.open(dump_path + str(counter) + '.jpg')
            pilImg = pilImg.resize((1080,1350))
            pilImg.save(dump_path + str(counter) + '.jpg')
            counter += 1
    else:
        print('Empty links list')

# Duplicating each image
def duplicateImg():
    for i in range(180):
        imgPath = 'D:/thick/Git/instaBot/igManager/images/honua/image' + str(i) + '.jpg'
        duplicatePath = 'D:/thick/Git/instaBot/igManager/images/honua2/image' + str(i) + '.jpg'
        with Image.open(imgPath) as f:
            duplicate = f.copy()
            duplicate.save(duplicatePath)

def duplicate_and_resize_image():
    for i in range(180):
        imgPath = 'D:/thick/Git/instaBot/igManager/images/honua/image' + str(i) + '.jpg'
        duplicatePath = 'D:/thick/Git/instaBot/igManager/images/honua11/image' + str(i) + '.jpg'
        with Image.open(imgPath) as f:
            duplicate = f.copy()
            duplicate = duplicate.resize((1080, 1350))

            duplicate.save(duplicatePath)

# Create philosophical quote overlay
def create_and_paste_overlay():
    for i in range(180):
        # Open background image
        backgroundImgPath = 'D:/thick/Git/Bots/instaBot/igManager/images/honua1/image' + str(i) + '.jpg'
        background = Image.open(backgroundImgPath)
        # Create overlay based on background image dimensions
        bgWidth, bgHeight = background.size
        width = math.ceil(bgWidth * .8)
        height = math.ceil(bgHeight * .8)
        textboxWidth = math.ceil(width * .8)
        textboxHeight = math.ceil(height * .8)

        # Overlay background image
        overlay = Image.new('RGBA', (width, height), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        # Opacity out of 255 (255=max opacity)
        OPACITY = 130
        overlay.putalpha(OPACITY)
        # Draw border around overlay
        overlay = ImageOps.expand(overlay, border=20, fill='black')
        
        # Configuring fonts (after resize); i had to do this manually before i realized all the images had to be 1080x1080 D:
        if len(quote[i]) <= 150:
            FONT_SIZE = 70
        elif len(quote[i]) > 150:
            FONT_SIZE = 50

        font_type = ImageFont.truetype('D:/thick/Git/Bots/instaBot/igManager/fonts/Mukta-Medium.ttf', FONT_SIZE)

        # Pasting the text
        draw = ImageDraw.Draw(overlay)

        charHeight = font_type.getsize('A')[1]

        currentXPos = (width - textboxWidth) / 2
        currentYPos = (height - textboxHeight) / 2
        widthTracker = 0

        for word in quote[i].split(' '):
            currentXPos = (width - textboxWidth) / 2 + widthTracker
            widthTracker += font_type.getsize(word + '  ')[0]

            if widthTracker >= textboxWidth:
                draw.text(xy=(currentXPos, currentYPos), text='\n', fill=(0,0,0), font=font_type)
                widthTracker = 0
                currentXPos = (width - textboxWidth) / 2
                currentYPos += charHeight
        
            draw.text(xy=(currentXPos, currentYPos), text=word + '  ', fill=(0,0,0), font=font_type)
            if widthTracker == 0:
                widthTracker += font_type.getsize(word + '  ')[0]

        draw.text(xy=((width - textboxWidth) / 2, currentYPos + charHeight * 2),
            text=author[i], fill=(0,0,0), font=font_type)
        
        # paste images onto duplicates
        backgroundCopy = background.copy()

        print(backgroundCopy.size)

        backgroundCopy.paste(overlay.copy(), (math.ceil((width - textboxWidth) / 2), math.ceil((height - textboxHeight) / 2)))

        # newWidth = 1080
        # newHeight = math.ceil((bgWidth / 1080) * bgHeight)
        
        # if newHeight > 1350:
        #     newHeight = 1350
        #     newWidth = math.ceil((bgHeight / 1350) * bgWidth)
        #     if newWidth > 1080:
        #         newWidth = 1080

        # backgroundCopy = backgroundCopy.resize((newWidth, newHeight))

        backgroundCopy.save(f'D:/thick/Git/Bots/instaBot/igManager/images/honua2/image{i}.jpg')

# Getting min and max widths and heights of image pool

def maxMinDimensions():
    minWidth = 99999
    minHeight = 99999

    maxWidth = 0
    maxHeight = 0

    for i in range(180):
        imgPath = 'D:/thick/Git/instaBot/igManager/images/honua2/image' + str(i) + '.jpg'
        with Image.open(imgPath) as f:
            w, h = f.size
            if w >= maxWidth:
                maxWidth = w
            elif w <= minWidth:
                minWidth = w
            if h >= maxHeight:
                maxHeight = h
            elif h <= minHeight:
                minHeight = h

    print('Min width: ' + str(minWidth))
    print('Min height: ' + str(minHeight))
    print('Max width: ' + str(maxWidth))
    print('Max height: ' + str(maxHeight))

# Max: 553 length of quote
# Min: 18 
# Min width: 1959 image dimensions
# Min height: 1365
# Max width: 8581
# Max height: 7952

# Getting and writing images of each philosopher; take size into account
def getPhilosophers():
    with open('D:/thick/Git/instaBot/igManager/philosophy-captions.txt', 'r') as f:
        for line in f:
            if line[0].isalpha():
               author.append(line.replace('\n', ''))

# Function calls go here
# create_and_paste_overlay()
