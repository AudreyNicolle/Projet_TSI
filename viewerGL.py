#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D,Text
import glutils
from mesh import Mesh
from collision import collision

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

    def run(self,vitesse):
        # boucle d'affichage*
        m = Mesh() 
        reboucle = True #pour pas reboucler quand on perd
        program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            testXG,testXD = collision.boucle_collision(self.objs[0],vitesse)
            '''if reboucle :
                if collision.boucle_collision(self.objs[0]):
                    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
                    vao = Text.initalize_geometry()
                    texture = glutils.load_texture('fontB.jpg')
                    o = Text('VOUS AVEZ', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
                    self.add_object(o)
                    o = Text('PERDU', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
                    self.add_object(o)
                    reboucle = False'''
            
            self.update_key(reboucle,testXG,testXD,vitesse)

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()

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

    def update_key(self,phase,testXG,testXD,vitesse):
        if phase: #utilise pour voir si on est en phase de jeu ou de défaite
            '''if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
                #self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
                self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.005

                self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])
            #    self.objs[0].transformation.translation += \
            #        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.08]))
            
            if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
                #self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
                self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.005

                self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])
            #    self.objs[0].transformation.translation -= \
            #        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.08]))'''
            
            if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
                #self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
                if not(testXG):
                    
                    if vitesse == 1:
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([-0.1, 0, 0]))
                    if vitesse == 2:
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([-0.2, 0, 0]))
                        

                    self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                    self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                    self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])

            if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
                if not(testXD):
                    #self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
                    if vitesse == 1 :
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
                    if vitesse == 2 :        
                        self.objs[0].transformation.translation -= \
                            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.2, 0, 0]))
                        

                    self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
                    self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.2
                    self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
                    self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
                    self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])

            if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
                self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
            if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
                self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
            if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
                self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
            if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
                self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
            
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
                vao = Text.initalize_geometry()
                texture = glutils.load_texture('fontB.jpg')
                o = Text('VOUS AVEZ', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
                self.add_object(o)
                o = Text('PERDU', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
                self.add_object(o)

            '''
            if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
                
                texture = glutils.load_texture('grassBlueSat.jpg')
                p0, p1, p2, p3 = [-2, 7, 7], [2, 7, 7], [2, 7, 9], [-2, 7, 9]
                p4, p5, p6, p7 = [-2, 6, 7], [2, 6, 7], [2, 6, 9], [-2, 6, 9]
                c = [1, 1, 1]

                m.vertices = np.array(self.creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
                m.faces = np.array(self.creation_faces_rectangulaire(), np.uint32)

                o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
                self.add_object(o)
            '''
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1

            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 15])

        # Mouvement de la cam
        # if glfw.KEY_Z in self.touch and self.touch[glfw.KEY_Z] > 0:
            # self.cam.transformation.translation += \
                # pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_, pyrr.Vector3([0, 0, 0.08]))
        # if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
        #     self.cam.transformation.translation -= \
        #         pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_y_rotation(self.cam.transformation.rotation_euler[pyrr.euler.index().yaw]), pyrr.Vector3([0, 0, 0.08]))