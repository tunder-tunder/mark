import matplotlib.pyplot as plt
import numpy as np

def negate(B):
    array= B.copy()
    return array*-1


def check(B,y,x):
    if not 0<= x < B.shape[1]:
        return False
    if not 0<= x < B.shape[0]:
         return False
    if B[y, x] !=0:
         return True
    return False

def neighbours2(B,y,x):
    left=y,x-1
    top=y-1,x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top=None
    return left,top


def  find(label, linked):
    j = label
    while linked[j] != 0:
        j=linked[j]
    return j

def union(label1, label2, linked):
    j=find(label1,linked)
    k=find(label2,linked)
    if j!=k:
        linked[k]=j


def recolor(image, prev_c, next_c):
    if prev_c != next_c:
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                if image[y,x] == prev_c:
                    image[y,x] = next_c
    return image


def remarked(image):
    
    before=[]

    for i in range(1, np.max(image) + 1):
        if i in image:
            before.append(i)
    
    new=[i for i in range(1, len(before) + 1)]
    
    for b, n in zip(before, new):
        image = recolor(image, b, n)
    return image

def two_pass_label(B):
    labeled=np.zeros_like(B)
    linked = np.zeros(len(B), dtype="uint16")
    label = 1
    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if B[y,x] != 0:
                n = neighbours2(B, y,x)
                if n[0] is None and n[1] is None:
                    m = label
                    label+=1
                else:
                    labels = [labeled[i] for i in n if i is not None]
                    m = min(labels)
                labeled[y,x] = m
                for i in n:
                    if i is not None:
                        lb = labeled[i]
                        if lb != m:
                            union(m, lb,linked)
    
    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            new_label= find(labeled[y,x], linked)
            if B[y,x] != labeled[y,x]:
                labeled[y,x] = new_label
            
    return remarked(labeled)

image = np.zeros((20,20), dtype="int32")

image[1:-1, -2]= 1

image[1,1:5] = 1 
image[1,7:12] = 1 
image[2,1:3] = 1 
image[2,6:8] = 1 
image[3:4,1:7] = 1

image[7:11,11] = 1 
image[7:11,14] = 1 
image[10:15,10:15] = 1

image[5:10,5] = 1 
image[5:10,6] = 1

labeled = two_pass_label(image)
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled, cmap="gist_rainbow")
plt.colorbar()
plt.show()