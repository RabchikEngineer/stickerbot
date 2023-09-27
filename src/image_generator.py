from PIL import Image,ImageDraw,ImageFont
import math, json, os

font_size=15
X_STEP=180
Y_STEP=240

with open('config.json', encoding='utf-8') as f:
    config=json.load(f)
directories=config["directories"]
debug=config["debug"]
background_color=tuple(config["colors"]["stickerlist_background"])

def create_stickerlist(filenames):

    num = len(filenames)
    sidex=math.ceil(math.sqrt(num))
    sidey=math.ceil(sidex-(sidex**2-num)/sidex)
    # print(sidex,sidey)
    # print(num)
    image = Image.new('RGBA', (sidex*X_STEP-20, sidey*Y_STEP), background_color)
    X,Y = 0,0
    for filename in filenames:
        names=filename[filename.find('#')+1:filename.rfind('.')].split('$')
        id=filename[:filename.find('#')]
        image_new_inner = Image.open(directories['stickers_dir'] + filename).convert('RGBA')
        image_new = Image.new('RGBA', (160, image_new_inner.size[1]+len(names)*20), background_color)
        image_new.paste(image_new_inner, (0,0), image_new_inner)
        x,y=0,image_new_inner.size[1]
        font = ImageFont.truetype(font='arial.ttf', size=font_size, encoding='unic')
        id_font = ImageFont.truetype(font='arial.ttf', size=font_size+10, encoding='unic')
        draw = ImageDraw.Draw(image_new)

        draw.text((0, 0), id, font=id_font,fill=(255,0,0,255))
        for name in names:
            draw.text((x, y), name, font=font)
            y+=20
        # image_new.save("temp/"+filename, "PNG")

        # print(X/X_STEP,Y/Y_STEP)
        image.paste(image_new,(X,Y))
        Y += Y_STEP if X>=X_STEP*(sidex-1) else 0
        X+=X_STEP if X<X_STEP*(sidex-1) else -X_STEP*(sidex-1)

    image.save(directories['temp_directory']+"stickerlist.png", "PNG")


#filenames=os.listdir("stickers")[:-10]
#create_stickerlist(filenames)
#print(*filenames, sep='\n')
