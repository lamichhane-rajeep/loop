import yaml
import math
import numpy as np
from matplotlib import pyplot as plt

configFile = "./settings.yaml"

def main():
    conf = None
    with open(configFile, "r") as stream:
        try:
            conf = yaml.safe_load(stream)
        except:
            exit(1)

    mat = initial(conf['graph'],conf['plotter'])
    f = writefile(conf['plotter'])
    cent = center(conf['graph'],conf['plotter'])
    loop(mat,cent,f,conf['graph'],conf['plotter'])

def initial(gconf,pconf):

    x = np.array ((20,0,10,20))
    y = np.array ((20,20,0,20))
    x = gconf['origin']['x']+(pconf['size']['width']/2)-(np.amax(x)-np.amin(x))/2+x
    y = gconf['origin']['y']+(pconf['size']['height']/2)-(np.amax(y)-np.amin(y))/2+y
    mat = np.row_stack((x,y))
    '''
    plt.plot(mat[0,:],mat[1,:])
    plt.xlim(-1,3)
    plt.ylim(-1,3)
    plt.show()
    '''
    return mat

def writefile(pconf):
    f = open(pconf['output'],'w').close
    return f

def center(gconf,pconf):
    x = gconf['origin']['x']+(pconf['size']['width']/2)
    y = gconf['origin']['y']+(pconf['size']['height']/2)

    cent = np.array ((x,y))
    return cent

def loop(mat,cent,f,gconf,pconf):
    l_num = gconf['number']
    sxy = np.array((gconf['translate']['x'],gconf['translate']['y']))
    gcode(mat,f,pconf)
    for x in range(l_num):
        rotate(mat,cent,gconf)
        scale(mat,cent,gconf,pconf)
        translate(mat,gconf)
        gcode(mat,f,pconf)
        cent[0] = cent[0] + sxy[0]
        cent[1] = cent[1] + sxy[1]
    return

def scale(mat,cent,gconf,pconf):
    s = (gconf['scale']['amount'])
    i = 0

    for x in mat[0,:]:
        if x > cent[0]:
            mat[0,i] = x + s
        elif x < cent[0]:
            mat[0,i] = x - s
        i += 1
    i = 0
    for x in mat[1,:]:
        if x > cent[1]:
            mat[1,i] = x + s
        elif x < cent[1]:
            mat[1,i] = x - s
        i += 1 

    return mat

def rotate(mat,cent,gconf):
    rot = gconf['rotation']['amount']
    i = 0
    for x in mat[0,:]:
        a = (cent[0] - mat[0,i]) * -1
        b = (cent[1] - mat[1,i]) * -1
        d = np.sqrt(np.power(a,2)+np.power(b,2))
        if a>0 and b>=0:
            theta = np.arctan(np.abs(b/a)) + np.deg2rad(rot) + 0
            mat[0,i] = np.cos(theta)*d+cent[0]
            mat[1,i] = np.sin(theta)*d+cent[1]
        elif a<=0 and b>0:
            theta = np.arctan(np.abs(a/b)) + np.deg2rad(rot) + np.deg2rad(90)
            mat[0,i] = np.cos(theta)*d+cent[0]
            mat[1,i] = np.sin(theta)*d+cent[1]
        elif a<0 and b<=0:
            theta = np.arctan(np.abs(b/a)) + np.deg2rad(rot) + np.deg2rad(180)
            mat[0,i] = np.cos(theta)*d+cent[0]
            mat[1,i] = np.sin(theta)*d+cent[1]
        elif a>=0 and b<0:
            theta = np.arctan(np.abs(a/b)) + np.deg2rad(rot) + np.deg2rad(270)
            mat[0,i] = np.cos(theta)*d+cent[0]
            mat[1,i] = np.sin(theta)*d+cent[1]
        i += 1

    return mat

def translate(mat,gconf):
    tx = (gconf['translate']['x'])
    ty = (gconf['translate']['y'])

    mat[0,:] = mat[0,:] + tx
    mat[1,:] = mat[1,:] + ty
    return mat

def gplunge(f,pconf):
    f = open(pconf['output'],'a')
    f.write('G1 F%f Z%f\n' % (pconf['speed']['plunge'],pconf['pen']['plunge']))
    f.close()
    return f

def gdraw(mat,f,pconf):
    f = open(pconf['output'],'a')
    i = 0
    for x in mat[0,:]:
        f.write('G1 F%f X%f Y%f\n' % (pconf['speed']['draw'],mat[0,i],mat[1,i]))
        i += 1
    f.close()
    return

def glift(f,pconf):
    f = open(pconf['output'],'a')
    f.write('G1 F%f Z%f\n' % (pconf['speed']['plunge'],pconf['pen']['lift']))
    f.close()
    return

def gtravel(mat,f,pconf):
    f = open(pconf['output'],'a')
    f.write('G1 F%f X%f Y%f\n' % (pconf['speed']['travel'],mat[0,0],mat[1,0]))
    f.close()
    return

def gcode(mat,f,pconf):
    gtravel(mat,f,pconf)
    gplunge(f,pconf)
    gdraw(mat,f,pconf)
    glift(f,pconf)

if __name__=="__main__":
    main()