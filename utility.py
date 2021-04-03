import cv2
import matplotlib.pyplot as plt

def showImage(img, title=''):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if(title != ''):
        plt.title(title)

    plt.imshow(img)
    plt.show()

def saveimage(img, img_name, path='output'):
    path = path + '/' + str(img_name) + '.jpg'
    cv2.imwrite(path, img)
    print('save image success !!')