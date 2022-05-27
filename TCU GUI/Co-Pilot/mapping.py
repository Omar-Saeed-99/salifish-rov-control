
import cv2
import numpy as np
def mapping():
    def click_event(event, x, y, flags, param):
        wr = 100
        img = cv2.imread('33.png')
        img = cv2.resize(img,(1000,1000))
        if event == cv2.EVENT_LBUTTONDOWN:
    
            #cv2.circle(img, (x, y), 3, (0, 0, 0), 1, cv2.FILLED)
            points.append((x, y))
            if len(points)%2 ==0 :
                ly  = int(abs(points[-1][1] - points[-2][1]))
                wx =  int(abs(points[-1][0] - points[-2][0]))

                if ly <40:
                    cv2.line(img, points[-1], points[-2], (19,69, 139), 10, cv2.LINE_AA)
                    ww = int(0.25*wx+min(points[-1][0],points[-2][0]))
                    ww2 = int(0.75*wx+min(points[-1][0],points[-2][0]))
                    #cv2.circle(img,(ww,points[-1][1]),3,[255,0,0],3)
                    #cv2.circle(img,(ww2,points[-1][1]),3,[255,0,0],3)
                    cv2.line(img,(ww,int(points[-1][1]+0.125*wx)),(ww,int(points[-1][1]-0.125*wx)),(19,69, 139), 10, cv2.LINE_AA)
                    cv2.line(img,(ww2,int(points[-1][1]+0.125*wx)),(ww2,int(points[-1][1]-0.125*wx)),(19,69, 139), 10, cv2.LINE_AA)

                elif wx <20:
                    cv2.line(img, points[-1], points[-2], (19,69, 139), 10, cv2.LINE_AA)
                    ll = int(0.25*ly+min(points[-1][1],points[-2][1]))
                    ll2 = int(0.75*ly+min(points[-1][1],points[-2][1]))
                    #cv2.circle(img,(ww,points[-1][1]),3,[255,0,0],3)
                    #cv2.circle(img,(ww2,points[-1][1]),3,[255,0,0],3)
                    cv2.line(img,(int(points[-1][0]+0.125*ly),ll,),(int(points[-1][0]-0.125*ly),ll,),(19,69, 139), 10, cv2.LINE_AA)
                    cv2.line(img,(int(points[-1][0]+0.125*ly),ll2,),(int(points[-1][0]-0.125*ly),ll2,),(19,69, 139), 10, cv2.LINE_AA)
                    #cv2.line(img,(ww2,int(points[-1][1]+0.125*wx)),(ww2,int(points[-1][1]-0.125*wx)),(19,69, 139), 10, cv2.LINE_AA)




                
                else:
                    if points[-1][0]>points[-2][0] and points[-1][1]>points[-2][1] or points[-1][0]<points[-2][0] and points[-1][1]<points[-2][1]:
                        cv2.line(img, points[-1], points[-2], (19,69, 139), 10, cv2.LINE_AA)
                        l = abs(int(abs(points[-1][1] - points[-2][1])*0.25) + min(points[-1][1],points[-2][1]))
                        w = abs(int(abs(points[-1][0] - points[-2][0])*0.25) + min(points[-1][0],points[-2][0]))
                    #  cv2.circle(img, (w, l), 10, (0, 0, 0), 1, cv2.FILLED)
                        ll = int(l-0.05*ly)
                        ww = int(w+0.22*wx)
                        #cv2.circle(img, (ww, ll), 10, (0, 0, 0), 1, cv2.FILLED)
                        ll2 = int(l+0.05*ly)
                        ww2= int(w-0.22*wx)
                        #cv2.circle(img, (ww2, ll2), 10, (0, 0, 0), 1, cv2.FILLED)
                        cv2.line(img,(ww,ll) ,(ww2,ll2), (19,69, 139), 10, cv2.LINE_AA)
                        

                        l2 = abs(int(abs(points[-1][1] - points[-2][1])*0.75) + min(points[-1][1],points[-2][1]))
                        w2 = abs(int(abs(points[-1][0] - points[-2][0])*0.75) + min(points[-1][0],points[-2][0]))
                        #cv2.circle(img, (w2, l2), 1, (0, 0, 0), 1, cv2.FILLED)
                        ll = int(l2-0.05*ly)
                        ww = int(w2+0.22*wx)
                        #cv2.circle(img, (ww, ll), 10, (0, 0, 0), 1, cv2.FILLED)
                        ll2 = int(l2+0.05*ly)
                        ww2= int(w2-0.22*wx)
                        cv2.line(img,(ww,ll) ,(ww2,ll2), (19,69, 139), 10, cv2.LINE_AA)

                    else:
                        cv2.line(img, points[-1], points[-2], (19,69, 139), 10, cv2.LINE_AA)
                

                        l = abs(int(abs(points[-1][1] - points[-2][1])*0.25) - max(points[-1][1],points[-2][1]))
                        w = abs(int(abs(points[-1][0] - points[-2][0])*0.25) + min(points[-1][0],points[-2][0]))
                        #cv2.circle(img, (w, l), 5, (0, 0, 0), 1, cv2.FILLED)

                        l2 = abs(int(abs(points[-1][1] - points[-2][1])*0.75) - max(points[-1][1],points[-2][1]))
                        w2 = abs(int(abs(points[-1][0] - points[-2][0])*0.75) + min(points[-1][0],points[-2][0]))
                        cv2.circle(img, (w2, l2), 5, (0, 0, 0), 1, cv2.FILLED)
                        ll = int(l+0.05*ly)
                        ww = int(w+0.22*wx)
                        #cv2.circle(img, (ww, ll), 10, (0, 0, 0), 1, cv2.FILLED)
                        ll2 = int(l-0.05*ly)
                        ww2= int(w-0.22*wx)
                        cv2.line(img,(ww,ll) ,(ww2,ll2), (19,69, 139), 10, cv2.LINE_AA)




                        ll = int(l2+0.05*ly)
                        ww = int(w2+0.22*wx)
                        #cv2.circle(img, (ww, ll), 10, (0, 0, 0), 1, cv2.FILLED)
                        ll2 = int(l2-0.05*ly)
                        ww2= int(w2-0.22*wx)
                        #cv2.circle(img, (ww2, ll2), 10, (0, 0, 0), 1, cv2.FILLED)
                        cv2.line(img,(ww,ll) ,(ww2,ll2), (19,69, 139), 10, cv2.LINE_AA)
                    
                #x = abs(points[-1][0]-points[-2][0])/wr
                

            cv2.imshow('Image', img)
            #cv2.imwrite('33.png', img)
        elif event == cv2.EVENT_RBUTTONDOWN:
            img = cv2.imread('33.png')
            img = cv2.resize(img,(1000,1000))
            
            



    img = cv2.imread('33.png')
    img = cv2.resize(img,(1000,1000))
    cv2.imshow('Image', img)
    points = []
    cv2.setMouseCallback('Image', click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()