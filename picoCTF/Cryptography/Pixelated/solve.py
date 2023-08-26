from PIL import Image

im1 = Image.open("./scrambled1.png")
im2 = Image.open("./scrambled2.png")

new = []
for T1, T2 in zip(im1.getdata(), im2.getdata()):
    (r, g, b) = (x ^ y for x, y in zip(T1, T2))
    
    if (r, g, b) == (255, 255, 255):
        (r, g, b) = (0, 0, 0)
    
    new += [(r, g, b)]

newim = Image.new(im1.mode, im1.size)
newim.putdata(new)

newim.save("flag.png")