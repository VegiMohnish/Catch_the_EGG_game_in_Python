from PIL import Image


img=input("Enter image name to resize\n")
ext=input("Image format\n")

im1=Image.open("resources/"+img+"."+ext)
width=int(input("Width"))
height=int(input("Height"))

outimg=im1.resize((width,height),Image.ANTIALIAS)

outimg.save("resources/resized_"+img+"."+ext)