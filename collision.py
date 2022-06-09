from cpe3d import Transformation3D

class collision:
    def boucle_collision(objc):
        posZ = objc.transformation.translation.z
        posX = objc.transformation.translation.x
        print(posZ)
        if posZ > -3 or posZ < -6 or posX > 15 or posX < -15:
            return True
        else :
            return False
        