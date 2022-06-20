
#!/usr/bin/env python3

#Import------------------------------------------------------------------------------------------
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D,Text
import glutils
import random
import time

#Classe------------------------------------------------------------------------------------------
class ViewerGL:
    
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}
        self.score = 0
        self.vitesse = 2
        self.max_time = 30
        self.start_time = time.time()
        self.reboucle = True #pour pas reboucler quand on perd
        self.score_win = 6

    def creation_plat_rectangulaire(self,p0,p1,p2,p3,p4,p5,p6,p7,c):
        nHaut=[0,1,0]
        nBas=[0,-1,0]
        nDroite=[0,0,-1]
        nGauche=[0,0,1]
        nDevant=[1,0,0]
        nDerriere=[-1,0,0]
        t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]

        verti = [[p0 + nHaut + c + t0], [p1 + nHaut + c + t1], [p2 + nHaut + c + t2], [p3 + nHaut + c + t3],
        [p4 + nBas + c + t0], [p5 + nBas + c + t1], [p6 + nBas + c + t2], [p7 + nBas + c + t3],
        [p0 + nGauche + c + t0], [p4 + nGauche + c + t1], [p7 + nGauche + c + t2], [p3 + nGauche + c + t3],
        [p3 + nDevant + c + t0], [p2 + nDevant + c + t1], [p6 + nDevant + c + t2], [p7 + nDevant + c + t3],
        [p0 + nDerriere + c + t0], [p1 + nDerriere + c + t1], [p5 + nDerriere + c + t2], [p4 + nDerriere + c + t3],
        [p1 + nDroite + c + t0], [p5 + nDroite + c + t1], [p6 + nDroite + c + t2], [p2 + nDroite + c + t3]]
        return verti

    def creation_faces_rectangulaire(self):
        faces = [[0, 1, 2], [0, 2, 3],
        [4, 5, 6], [4, 6, 7],
        [8, 9, 10], [8, 10, 11],
        [12, 13, 14], [12, 14, 15],
        [16, 17, 18], [16, 18, 19],
        [20, 21, 22], [20, 22, 23]]
        return faces

    def run(self):
        
        #initialisation affichage score 
        programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
        vao = Text.initalize_geometry()
        texture = glutils.load_texture('fontB.jpg')
        o = Text('Score : ' + str(self.score), np.array([-0.8, 0.3], np.float32), np.array([0.4, 0.4], np.float32), vao, 2, programGUI_id, texture)
        self.add_object(o)

         
        
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            if self.score < self.score_win: # si le score est inferieur au score pour gagner il test si le temps imparti n'est pas depasse
                if time.time() - self.start_time > self.max_time and self.reboucle: #si le temps imparti est dépassé il efface le score et met en gros "vous avez perdu"
                    del self.objs[-1]
                    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
                    vao = Text.initalize_geometry()
                    texture = glutils.load_texture('fontB.jpg')
                    o = Text('VOUS AVEZ', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
                    self.add_object(o)
                    o = Text('PERDU', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
                    self.add_object(o)
                    self.reboucle = False #reboucle devient false pour eviter des actions en trop comme le reaffichage du message et l'update des keys du joueur
            else : #si le score est egal il met "vous avez gagne"
                del self.objs[-1]
                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
                vao = Text.initalize_geometry()
                texture = glutils.load_texture('fontB.jpg')
                o = Text('VOUS AVEZ', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
                self.add_object(o)
                o = Text('GAGNE', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
                self.add_object(o)
                self.reboucle = False #reboucle devient false pour les memes raisons que precedemment

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()
            
            #appel des fonctions de gestion  des mouvements des objets et
            # des interractions entre les objets, affichage objet 2D
            testXG,testXD = self.collision()
            self.mvt()
            self.update_key(testXG,testXD)
            if self.reboucle:
                self.affichage_score()
            
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    
    def update_key(self,testXG,testXD,):
        if self.reboucle :
            if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0: # test si la touche gauche est enfonce/on appuie dessus
                if not(testXG): # test si le personnage n'est pas deja au bout de la plateforme
                        
                    if self.vitesse == 1:
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([-0.1, 0, 0]))
                    if self.vitesse == 2:
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([-0.2, 0, 0]))
                            

                    self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                    self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                    self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])

            if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
                if not(testXD):
                    if self.vitesse == 1 :
                        self.objs[0].transformation.translation -= \
                                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
                    if self.vitesse == 2 :        
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.2, 0, 0]))
                            

                    self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                    self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                    self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])

            
            #emission du projectile a l'appuie de la touche
            if glfw.KEY_Z in self.touch and self.touch[glfw.KEY_Z] > 0 :
                #lorsqu'on appuie on fait apparaitre l'objet et on lui donne en
                #position initiale celle du stegosaure
                if self.objs[1].visible == False :
                    self.objs[1].transformation.translation  = self.objs[0].transformation.translation.copy()                       
                    self.objs[1].transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy()
                    self.objs[1].visible = True
            
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1

            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15]) 
      
      
    """
    @brief : cette méthode permet de gérer le mouvement du projectile et des ennemis.
            
    @param : none
    
    @return : none
    """             
    def mvt(self) :
        
        #mouvement du projectile
        if self.objs[1].visible == True :
            self.objs[1].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.\
                    create_from_eulers(self.objs[1].transformation.\
                    rotation_euler), pyrr.Vector3([0, 0, 0.2]))
        
        #mouvement des ennemis
        for i in range(3,6) :
            if self.objs[i].visible == True :
                self.objs[i].transformation.translation += self.objs[i].sens*\
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.\
                    create_from_eulers(self.objs[1].transformation.\
                    rotation_euler), pyrr.Vector3([0.03, 0, 0.0]))
   
   
    """
    @brief : cette méthode permet de gérer les collisions :
            - entre le joueur et les bords de sa plateforme
            - entre le projectile et les ennemis
            - entre les ennemis et les bords de leur plateforme.
            - entre le projectile et la fin de la platerforme
            
    @param : none
    
    @return :
                testXG : permet de savoir si le joueur a atteint le bord gauche (booléen) 
                testXD : permet de savoir si le joueur a atteint le bord droit (booléen) 
    """     
    def collision(self) : 
        
        #on teste les collions entre le projectile et les ennemis qui dans la liste slef.objs
        #sont aux indices 4,5,6. On verifie si les ennemis touche les bords de la plateforme.
        for i in range(3,6) :
            #on vérifie si l'ennemi et le projectile sont sur la même profondeur (axe z) et sur 
            # la même ligne (axe x)
            if round(self.objs[1].transformation.translation.z,1) == self.objs[i].transformation.translation.z and \
                round(self.objs[1].transformation.translation.x,1) - 0.5 < self.objs[i].transformation.translation.x \
                < round(self.objs[1].transformation.translation.x,1) + 0.5 :
                #si oui, augmente le score, rend le projectile non visible, le réinitailise à la positon du joueur
                #on rend l'enenemi non visible, on change sa position sur la ligne, on le rend visible
                if i == 3:
                    self.score += 1
                if i == 4 :
                    self.score += 2
                else : 
                    self.score += 3
                self.objs[1].visible = False
                self.objs[1].transformation.translation  = self.objs[0].transformation.translation.copy()                       
                self.objs[1].transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy()
                self.objs[i].visible = False
                self.objs[i].transformation.translation.x = -3 + random.random()*15
                self.objs[i].visible = True

            #si l'ennemi touche les bords, on change le sens de sa direction
            if self.objs[i].transformation.translation.x  < -11.0 :
                self.objs[i].sens = +1
            
            if self.objs[i].transformation.translation.x > 11.0 :
                self.objs[i].sens = -1

        #si le projectile touche le fond de la plateforme ennemi, on la réinitialise
        if round(self.objs[1].transformation.translation.z,1) == 23.0 :
            self.objs[1].transformation.translation  = self.objs[0].transformation.translation.copy()                       
            self.objs[1].transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy()
            self.objs[1].visible = False

        #on verifie si le joueur touche les bords de sa plateforme
        posX =self.objs[0].transformation.translation.x
        posX = self.objs[0].transformation.translation.x
        testXG=False
        testXD=False
        if self.vitesse == 1:
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


    """
    @brief : cette méthode permet d'afficher le score. On change de programme pour sélectionner
            celui qui permet "d'écrire" en 2D. L'objet créé, le dernier de la liste self.objs, 
            pour cette affichage est supprimé et rajouté à chaque tour.
            
    @param : none
    
    @return : none
    """     
    def affichage_score(self):
        
        del self.objs[-1]
        programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
        vao = Text.initalize_geometry()
        texture = glutils.load_texture('fontB.jpg')
        o = Text('Score : ' + str(self.score), np.array([-0.8, 0.3], np.float32), np.array([0.4, 0.4], np.float32), vao, 2, programGUI_id, texture)
        self.add_object(o)


        
                

            
