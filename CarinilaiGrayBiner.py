# Import the PIL library - pip3 install Pillow
from PIL import Image
import turtle

# Open our image
im = Image.open("warpeadthresh7.jpg")

# Convert our image to RGB
rgb_im = im.convert('RGB')

# Use the .size object to retrieve a tuple contain width,height of the image
# and assign them to width and height variables
width = rgb_im.size[0]
height = rgb_im.size[1]

# set some counters for current row and column and total pixels
row = 1
col = 1
pix = 0

# create an empty output row
rowdata = ""

# set up our turtle variables
sqsize = 2
turtle.colormode(255)
turtle.speed(0)

# loop through each pixel in each row outputting RGB value as we go...
while row < height + 1:
    print("")
    print("Row number: " + str(row))
    while col < width + 1:
        r, g, b = rgb_im.getpixel((col - 1, row - 1))
        rowdata += "(" + str(r) + "," + str(g) + "," + str(b) + ") "
        turtle.pendown()
        turtle.fillcolor(r, g, b)
        turtle.pencolor(r, g, b)
        if sqsize > 1:
            turtle.begin_fill()
            for i in range(4):
                turtle.forward(sqsize)
                turtle.right(90)
            turtle.end_fill()
        else:
            turtle.forward(sqsize)
        turtle.penup()
        if sqsize > 1:
            turtle.forward(sqsize)
        col = col + 1
        pix = pix + 1
    turtle.backward(sqsize * width)
    turtle.right(90)
    turtle.forward(sqsize)
    turtle.left(90)
    print(rowdata)
    rowdata = ""
    row = row + 1
    col = 1