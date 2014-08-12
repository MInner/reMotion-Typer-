import time

from SimpleCV import Image, BlobMaker, Color, Camera

# name = "img1.jpg"
# img = Image(name)
# img.show()
# time.sleep(1)

th = 240
n = 0
while True:
    c = Camera(0)
    img = c.getImage()
    img.show()

    # print("New image")

    # print(th)
    # bm = BlobMaker() # create the blob extractor
    # img.invert().binarize(thresh=th).invert().show()
    # time.sleep(0.1)

    # blobs = bm.extractFromBinary(img.invert().binarize(thresh=th).invert(),img, minsize = 200)

    # print(len(blobs))
    # if len(blobs) == 0:
    #     th = th - 10
    #     continue

    # if(len(blobs)>0 and len(blobs) < 10): # if we got a blob
    #     for i, b in enumerate(blobs[::-1]):
    #         print("Blob %d" % i)
    #         if b.isCircle(0.4):
    #             # b.draw(color=Color.RED,width=-1)
    #             img.drawCircle(b.centroid(),30,color=Color.BLUE)
    #             # time.sleep(0.5)
    #             # img.save('eye_%d.jpg' % n)
    #             # n = n + 1
    #         print(b.circleDistance())
    #         img.show()
    #         # time.sleep(0.1)