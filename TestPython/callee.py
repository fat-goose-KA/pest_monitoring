import cv2;
import numpy as np;
def roi(img_file, thresh_size,imageShow):  #img_file: file name
    # print(img_file)
    im_in = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    if im_in is None:
        raise NameError('in roi function, incorrect filename, address or empty file')
    th, im_th = cv2.threshold(im_in, 150, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = im_in.copy()
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_in, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv
    cv2.imshow("Foreground", im_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()     #for check whether filtering has proccessed well
    th, im_twocol = cv2.threshold(im_out, 150, 255, cv2.THRESH_BINARY)   ## use  filter again

    cv2.imshow("adfadad", im_twocol)
    cv2.waitKey(0)
    cv2.destroyAllWindows()     #for check whether filtering has proccessed well

    kernel = np.ones((8,8),np.uint8)
    closing = cv2.morphologyEx(im_twocol, cv2.MORPH_CLOSE, kernel)    
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    th, im_otsu = cv2.threshold(closing, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    output= cv2.connectedComponentsWithStats(im_otsu) # 4 or 8
    # def drawbox(im, stats):
    #     for i in range(1,stats[0]):
    #         print("huh")
    #         x0=stats[2][i,cv2.CC_STAT_LEFT]
    #         y0=stats[2][i,cv2.CC_STAT_TOP]
    #         x=stats[2][i,cv2.CC_STAT_WIDTH]
    #         y=stats[2][i,cv2.CC_STAT_HEIGHT]
    #         cv2.rectangle(im,(x0,y0),(x0+x,y0+y),(255,255,255),10)
    # drawbox(im_otsu, output)
    cv2.imshow("otsu",im_otsu)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result=[]
    im_origin = cv2.imread(img_file, cv2.IMREAD_COLOR)
    for i in range(1,output[0]):
        # print("huh")
        if (output[2][i,cv2.CC_STAT_AREA]<thresh_size):
            continue
        x0=output[2][i,cv2.CC_STAT_LEFT]
        y0=output[2][i,cv2.CC_STAT_TOP]
        x=output[2][i,cv2.CC_STAT_WIDTH]
        y=output[2][i,cv2.CC_STAT_HEIGHT]
        cv2.rectangle(im_otsu,(x0,y0),(x0+x,y0+y),(255,255,255),10)
        if imageShow == True:
            cv2.imshow("otsu",im_otsu)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # subimg=im_origin[x:x+x0, y:y+y0]
        subimg=im_origin[y0:y+y0,x0:x+x0]
        result.append(subimg)
        if imageShow == True:
            cv2.imshow("sub",subimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
    # print(result)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~`")
    if imageShow == True:
        for i in result:
            cv2.imshow("return",i)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return result
# roi("./6.jpg",5000)
# roi("./test.png",5000)