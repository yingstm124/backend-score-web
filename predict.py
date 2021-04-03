from pre_processing import *
from segmentation import *
from utility import *

from keras.models import load_model

import cv2


class Predict:
    
    def __init__(self, img, debug=False):
        self.debug = debug
        self.image = img
        self.model = load_model('model/mnist.h5')

    def getResult(self):
        predicts = self.model.predict(self.image.reshape(1,28,28,1))
        result = np.argmax(predicts)

        if(self.debug):
            print('result --> ',result)
            showImage(self.image, 'image')

        return result


if __name__ == '__main__':
    
    img = cv2.imread('image_test/test8.jpg')
    showImage(img, 'original image')
    binary_image = Pre_Processing(img,True).getBinaryImage()

    digit_list, score_box = Segmentation(binary_image,True).getID_ScoreBox()
    print("len digit :",len(digit_list))
    print("len score : ",len(score_box))

    # student ID
    result_std = ''
    count = len(digit_list)
    for d in digit_list:

        result = str(Predict(d,True).getResult())
        result_std += result

    
        
    # score
    count = len(score_box)
    result_score = ''
    if(count != 0):
        for s in score_box:
            result = str(Predict(s,True).getResult())
            result_score += result
            count -= 1
    else: 
        result = 0

    result_score = int(result_score)

    print('result student id ', result_std)
    print('result score ',result_score)