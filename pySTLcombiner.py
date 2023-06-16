import numpy as np
from stl import mesh
import os
import stl

def combine_stl(meshes, save_path):
    combined = mesh.Mesh(np.concatenate([m.data for m in meshes]))
    combined.save(save_path, mode=stl.Mode.ASCII)
    
def combine_stl_side_by_side(meshes, paths, save_path):
    if meshes == None or len(meshes) == 0:
        print("No Meshes.")
        return
    nTotalCount = len(meshes)
    idx = 0
    while(True):
        gap_size = meshes[idx].x.max() - meshes[idx + 1].x.max() + 10
        meshes[idx + 1].x = meshes[idx + 1].x + np.ones(meshes[idx + 1].x.shape) * gap_size
        if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
        idx += 1
        if idx > nTotalCount - 2:
            break
    if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
    combine_stl(meshes, save_path)
    
if __name__ == '__main__':
    strInput = input('Input word to make\n')
    
    direc = os.getcwd()
    filesSTL = []
    strOutPath = strInput + '.stl'
    inputFailed = False
    for c in strInput:
        if c.isnumeric():
            filesSTL.append(os.path.join(direc, 'number\\' + c + '.stl'))
        elif c.isupper():
            filesSTL.append(os.path.join(direc, 'upper\\' + c + '.stl'))
        elif c.islower():
            filesSTL.append(os.path.join(direc, 'lower\\' + c + '.stl'))
        else:
            inputFailed = True
            break
    
    if inputFailed:
        print("Input word correctly")
    else:
        meshes = []
        paths = []
        for path in filesSTL:
            meshes.append(mesh.Mesh.from_file(path))
            paths.append(path)
        combine_stl_side_by_side(meshes, paths, strOutPath)
        print('Output to ' + strOutPath + '\n') 
    input('Press Enter to exit.')