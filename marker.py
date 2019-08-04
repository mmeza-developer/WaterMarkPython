#! python3
# marker.py - Automates basic image manipulation:  resize, watermark, and compress images.

import argparse
import shutil
import os
import os.path
import ast

from datetime import datetime

try:
    import tinify
except ImportError:
    exit("This script requires the tinify module.\nInstall with pip install tinify")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:    
    exit("This script requires the PIL module.\nInstall with pip install Pillow")

def compress_image(filename):    
    tinify.key = "YOUR_API_KEY"
    source = tinify.from_file(filename)
    source.to_file(filename)

def resize_image(image, width, height):
    imageWidth, imageHeight = image.size

    if width is None and height is not None:
        imageWidth = (imageWidth * height) / imageHeight
        imageHeight = height
    elif width is not None and height is None:
        imageHeight = (imageHeight * width) / imageWidth
        imageWidth = width
    elif width is not None and height is not None:
        imageWidth = width
        imageHeight = width

    return image.resize((int(imageWidth), int(imageHeight)), Image.ANTIALIAS)

def jpgToPng(filename,directory):
    if not filename.lower().endswith(".png"):
        image=Image.open(filename,"r")
        filename=filename.replace(".jpg",".png")
        image.save(directory+"\\"+filename,"png")
    else:
        shutil.copy(filename,directory);  

def copyJpg(filename,directory):
   
    if filename.lower().endswith(".png"):
        print(filename)
        image=Image.open(filename,"r")
        image=image.convert("RGB")
        filename=filename.replace(".png",".jpg")
        image.save("..\\"+directory+"\\"+filename,"JPEG")
                     
    

def watermark_image_with_logo(filename, filenameLogo):
    image=None;
    imageLogo=None;
    resizedImageLogo=None;
    if filename.lower().endswith('.png'):
        image = Image.open(filename).convert('RGBA')
    else:
        image = Image.open(filename).convert('RGB')

    if filenameLogo is not None:
        imageLogo=Image.open(filenameLogo).convert('RGBA');
           
    
    width, height = image.size
    widthLogo, heightLogo = imageLogo.size

    porporcionHeight=int(((width/5)*heightLogo)/widthLogo)
    resizedImageLogo=resize_image(imageLogo,int(width/5),porporcionHeight)
    widthImageLogo,heightImageLogo=resizedImageLogo.size; 
    
    image.paste(resizedImageLogo,(int(width-widthImageLogo),0),mask=resizedImageLogo)
   
    return image


def watermark_image_with_text(image,filename, text,color):
    imageWatermark=None
  
    imageWatermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
    

    draw = ImageDraw.Draw(imageWatermark)
    
    width, height = image.size
    font = ImageFont.truetype("impact.ttf", int(height / 15))
    textWidth, textHeight = draw.textsize(text, font)
    x = int(width/2)-int(textWidth/2)
    y = int(height/2)-int(textHeight/2)
    draw.text((x, y), text, font=font,fill=color)
    x = int(width/2)-int(textWidth/2)
    y = int(height/4)-int(textHeight/2)
    draw.text((x, y), text, font=font,fill=color)
    x = int(width/2)-int(textWidth/2)
    y = (int(height-(height/4)))-int(textHeight/2)
    draw.text((x, y), text, font=font,fill=color)

    imageWatermark=imageWatermark.rotate(45)
   
    return Image.alpha_composite(image, imageWatermark)
    
    

def main():
    parser = argparse.ArgumentParser(description='Automates basic image manipulation.')
    parser.add_argument('directory', nargs='?', default='.', help='Directorio con las imagenes que se desean procesar')
    parser.add_argument('-c', '--color',default='(239,239,239,128)', type=ast.literal_eval, help="Color seleccionado para el texto, este debe ser ingresado asi: (R,G,B,A), donde R,G,B son números del 0 al 255 y A es un numero de 0 a 1")
    parser.add_argument('-t', '--text', help="Texto para la Marca de Agua")
    parser.add_argument('-i', '--image-overlay', help="Imagen png transparent para insertar en la esquina superior derecha de todas las imagenes")
   
    args = parser.parse_args()
    
    shutil.copytree(os.getcwd(),'directory_backup_{1}'.format(args.directory, datetime.now().isoformat()).replace(':', '_'))
    directoryPng="png-files"
    directoryJpg="jpg-files"
    try: 
        os.mkdir(directoryPng)
    except OSError:
        if not os.path.isdir(directoryPng):
            raise

    try: 
        os.mkdir(directoryJpg)
    except OSError:
        if not os.path.isdir(directoryPng):
            raise

                  
    imageFileOperation(args,directoryPng,directoryJpg)    

def imageFileOperation(args,directoryCopy,directoryJpgCopy):
    os.chdir(args.directory)

    for filename in os.listdir():
        
        if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
           jpgToPng(filename,directoryCopy)
            
    os.chdir(directoryCopy)

    for filename in os.listdir():
        
        if filename.lower().endswith('.png'):
           
            if args.image_overlay is not None:
                watermarked_image = watermark_image_with_logo(filename, args.image_overlay)
                watermarked_image= watermark_image_with_text(watermarked_image,filename,args.text,args.color)
                watermarked_image.save(filename)
                copyJpg(filename,directoryJpgCopy)
        else:
            print("No es png: ",filename) 

    
                    
                       

           
if __name__ == '__main__':
    main()