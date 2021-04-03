digit_list, score_box = Segmentation(binary_image,True).getID_ScoreBox()
    print("len digit :",len(digit_list))
    print("len score : ",len(score_box))

    # student ID
    result_std = ''
    count = len(digit_list)
    for d in digit_list:

        result = str(Predict(d,True).getResult())
        result_std += result

    print('result student id ', result_std)
        
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
    print('result score ',result_score)