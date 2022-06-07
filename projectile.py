#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:35:23 2022

@author: audrey.nicolle
"""
#Import -----------------------------------------------------------------------
import numpy as np
import OpenGL.GL as GL
import pyrr

#Classe -----------------------------------------------------------------------
class Projectile () :
    
    def __init__ (self,a0, a1, a2, b0, b1, b2, c0, c1, c2) :   
        print("here")
        sommets = np.array(((a0, a1, a2), (b0, b1, b2), (c0, c1, c2)), np.float32)
        # attribution d'une liste d' ́etat (1 indique la cr ́eation d'une seule liste)
        vao = GL.glGenVertexArrays(1)
        # affectation de la liste d' ́etat courante
        GL.glBindVertexArray(vao)
        # attribution d’un buffer de donnees (1 indique la cr ́eation d’un seul buffer)
        vbo = GL.glGenBuffers(1)
        # affectation du buffer courant
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        # copie des donnees des sommets sur la carte graphique
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)
        # Les deux commandes suivantes sont stox += 0.01ck ́ees dans l' ́etat du vao courant
        # Active l'utilisation des donn ́ees de positions
        # (le 0 correspond `a la location dans le vertex shader)
        GL.glEnableVertexAttribArray(0)
        # Indique comment le buffer courant (dernier vbo "bindé")
        # est utilis ́e pour les positions des sommets
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)