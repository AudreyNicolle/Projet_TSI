from cpe3d import Transformation3D

class collision:
    def boucle_collision(objc,vitesse):
        
        posX = objc.transformation.translation.x
        testXG=False
        testXD=False
        print(posX)
        if vitesse == 1:
            if posX > 13 :
                testXG = True
            elif posX < -12.5 :
                testXD = True
            return testXG,testXD
        else :
            if posX > 12.9 :
                testXG = True
            elif posX < -12.4 :
                testXD = True
            return testXG,testXD
        