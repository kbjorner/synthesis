from PIL import Image, ImageDraw
import re

pix_reg = re.compile("b(\d+)_(\d+)")

with open(input("File to analyze: "), "r") as f:
    matches = pix_reg.findall(f.read())

img = Image.new("RGB", (560, 560), color="white")
draw = ImageDraw.Draw(img, "RGBA")

def draw_pixel(draw, pos, size):
    pos_x = pos[0] * size
    pos_y = pos[1] * size
    draw.rectangle([(pos_x, pos_y), (pos_x + (size - 1), pos_y + (size - 1))], fill=(255, 102, 0, 100))

def draw_border(img, draw):
    draw.rectangle([(0, 0), (img.width - 1, img.height - 1)], outline="black", width=10)

for pix in matches:
    pix = [int(coord) for coord in pix]
    draw_pixel(draw, (pix[0], pix[1]), 20)

#draw_border(img, draw)

img.save("heat.png")
print(matches)
