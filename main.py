#Import-------------------------------------------------------------------------------------------------------------
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

#Fonction__--------------------------------------------------------------------------------------------------------
def creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c):
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

def creation_faces_rectangulaire():
    faces = [[0, 1, 2], [0, 2, 3],
    [4, 5, 6], [4, 6, 7],
    [8, 9, 10], [8, 10, 11],
    [12, 13, 14], [12, 14, 15],
    [16, 17, 18], [16, 18, 19],
    [20, 21, 22], [20, 22, 23]]
    return faces

#Main-------------------------------------------------------------------------------------------------------------
def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1.5, 1.5, 1.5, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('stegosaurus.jpg')
    vaoNow = m.load_to_gpu()
    o = Object3D(vaoNow, m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    m = Mesh.load_obj('cube_ge.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('carre.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    o.visible = False
    viewer.add_object(o)


    #plateforme principale
    texture = glutils.load_texture('grass.jpg')

    #la taille de la platforme est changée
    m = Mesh()
    p0, p1, p2, p3 = [-15, 0, -3], [15, 0, -3], [15, 0, -6], [-15, 0, -6]
    p4, p5, p6, p7 = [-15, -1, -3], [15, -1, -3], [15, -1, -6], [-15, -1, -6]
    c = [1, 1, 1]

    
    
    m.vertices = np.array(creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
    m.faces = np.array(creation_faces_rectangulaire(), np.uint32)
    
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #plateforme ennemie
    texture = glutils.load_texture('grassBlueSat.jpg')
    p0, p1, p2, p3 = [-12, 0, 7], [12, 0, 7], [12, 0, 23], [-12, 0, 23]
    p4, p5, p6, p7 = [-12, -1, 7], [12, -1, 7], [12, -1, 23], [-12, -1, 23]
    c = [1, 1, 1]

    m.vertices = np.array(creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
    m.faces = np.array(creation_faces_rectangulaire(), np.uint32)

    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    # vao = Text.initalize_geometry()
    # texture = glutils.load_texture('fontB.jpg')
    # o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)
    # o = Text('3ETI', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)
    
    #stegosaure mechant
    for i in range(3):
            m = Mesh.load_obj('stegosaurus.obj')
            m.normalize()
            m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
            tr = Transformation3D()
            tr.translation.y = -np.amin(m.vertices, axis=0)[1]
            tr.translation.z = 10+4*i
            tr.translation.x = -3 + 3*i
            tr.rotation_center.z = 0.1
            tr.rotation_euler[pyrr.euler.index().yaw] = np.pi
            texture = glutils.load_texture('stegosaurus.jpg')
            o = Object3D(vaoNow, m.get_nb_triangles(), program3d_id, texture, tr)
            viewer.add_object(o)
    #création méchants stegosaures
    
    
    #la taille de la platforme est changée
    #plateforme principale
    texture = glutils.load_texture('grass.jpg')
    m = Mesh()
    p0, p1, p2, p3 = [-13, 0, -3], [13.5, 0, -3], [13.5, 0, -6], [-13, 0, -6]
    p4, p5, p6, p7 = [-13, -1, -3], [13.5, -1, -3], [13.5, -1, -6], [-13, -1, -6]
    c = [1, 1, 1]
    p8, p9, p10, p11 = [-13, 0, -3], [13.5, 0, -3], [13.5, 0, -6], [-13, 0, -6]
    p12, p13, p14, p15 = [-13, -1, -3], [13.5, -1, -3], [13.5, -1, -6], [-13, -1, -6]
    
    m.vertices = np.array(creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
    m.faces = np.array(creation_faces_rectangulaire(), np.uint32)
    
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #plateforme ennemie
    texture = glutils.load_texture('grassBlueSat.jpg')
    p0, p1, p2, p3 = [-12, 0, 7], [12, 0, 7], [12, 0, 23], [-12, 0, 23]
    p4, p5, p6, p7 = [-12, -1, 7], [12, -1, 7], [12, -1, 23], [-12, -1, 23]
    c = [1, 1, 1]

    m.vertices = np.array(creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
    m.faces = np.array(creation_faces_rectangulaire(), np.uint32)

    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #barriere
    p0, p1, p2, p3 = [-13, 0.3, -3], [-12.5, 0.3, -3], [-12.5, 0.3, -3.5], [-13, 0.3, -3.5]
    p4, p5, p6, p7 = [-13, 0, -3], [-12.5, 0, -3], [-12.5, 0, -3.5], [-13, 0, -3.5]
    c = [1, 1, 1]
    p8, p9, p10, p11 = [-12.5, 0.2, -3.2], [-12, 0.2, -3.2], [-12, 0.2, -3.3], [-12.5, 0.2, -3.3]
    p12, p13, p14, p15 = [-12.5, 0.1, -3.2], [-12, 0.1, -3.2], [-12, 0.1, -3.3], [-12.5, 0.1, -3.3]
    vect = 0
    for i in range(27):
        texture = glutils.load_texture('wood.jpg')
        p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0] = p0[0]+vect, p1[0]+vect, p2[0]+vect, p3[0]+vect, p4[0]+vect, p5[0]+vect, p6[0]+vect, p7[0]+vect 
        m.vertices = np.array(creation_plat_rectangulaire(p0,p1,p2,p3,p4,p5,p6,p7,c), np.float32)
        m.faces = np.array(creation_faces_rectangulaire(), np.uint32)
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
        viewer.add_object(o)
        if i !=26:
            p8[0], p9[0], p10[0], p11[0], p12[0], p13[0], p14[0], p15[0] = p8[0]+vect, p9[0]+vect, p10[0]+vect, p11[0]+vect, p12[0]+vect, p13[0]+vect, p14[0]+vect, p15[0]+vect 
            m.vertices = np.array(creation_plat_rectangulaire(p8,p9,p10,p11,p12,p13,p14,p15,c), np.float32)
            m.faces = np.array(creation_faces_rectangulaire(), np.uint32)
            o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
            viewer.add_object(o)
        vect = 1
        
    viewer.run()

if __name__ == '__main__':
    main()
