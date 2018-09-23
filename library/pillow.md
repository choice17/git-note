# PILLOW PIL

* **Content**  
* **[image](#image)**  
* **[imagefont](#imagefont)**  
* **[imagedraw](#imagedraw)**  
* **[palette](#palette)**  

[referece](d)

## image  

Image module is exchangable to numpy array  

```python 
from PIL import Image  

img = Image.open(fname)

img_np = np.array(img)

Image.fromarray(img_np)

# type: "L" - monotonic, "RGB", "BGR", "RGBA", "1", "P", "YUV"    
img = Image.new({type:str}, (w, h), (1))

# for Image class  

# to string 
img.getdata()

# get channel 
img.getchannel({channel:int})

# put data  
img.putdata({string})  

# convert 
img.convert({type:str})  

# save  
img.save({jpg, png, bmp: with .{format})

# display
img.show()

```  

## imagefont  

## imagedraw 


enable to draw font with specific truetype font style  

```python  
[M O8from PIL import Image, ImageFont, ImageDraw  
fontfile = 'font.ttf'
font = ImageFont.truetype(fontfile, {textsize:float})
img = Image.new("RGBA", (w, h), {bgcolor:(0,255,0)})

text = chr(ascii_idx)
draw = ImageDraw.Draw(img)
textw, texth = draw.textsize(text, font)
draw.text((textw, texth), text:str, textcolor:(r,g,b), font=font)

ImageDraw.Draw(img)
```



