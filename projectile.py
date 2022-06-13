#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:35:23 2022

@author: audrey.nicolle
"""
#!/usr/bin/env python3

#Import------------------------------------------------------------------------
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import projectile as p

#Class------------------------------------------------------------------------
class Projectile (Object3D):

    def __init__ (self) :
        
        print("Dans classe projectile")
        program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
        # programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag') 
        
        m = Mesh.load_obj('cube_ge.obj')
        #m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -5
        tr.rotation_center.z = 0.2
        texture = glutils.load_texture('carre.jpg')
        Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        
        
