#!/usr/bin/env python
import sys
import Image
import numpy



if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    width = im.size[0]
    height = im.size[1]
    imarray = numpy.array(im)
    new = Image.fromarray(imarray)
    new.save(sys.argv[2])
    


