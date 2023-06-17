import numpy as np
from stl import mesh
import os
import stl
import sys
import math

def combine_stl(meshes, save_path):
    combined = mesh.Mesh(np.concatenate([m.data for m in meshes]))
    combined.save(save_path, mode=stl.Mode.ASCII)
        
def combine_stl_horizontally(meshes, paths, save_path, add_gap_size):
    if meshes == None or len(meshes) == 0:
        print("No Meshes.")
        return
    nTotalCount = len(meshes)
    idx = 0
    while(True):
        sec_x_min_pos = meshes[idx].x.max() + add_gap_size
        gap_size = sec_x_min_pos - meshes[idx + 1].x.min()
        
        meshes[idx + 1].x = meshes[idx + 1].x + np.ones(meshes[idx + 1].x.shape) * gap_size
        if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
        idx += 1
        if idx > nTotalCount - 2:
            break
    if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
    combine_stl(meshes, save_path)

def combine_stl_h_brick(meshes, brick_path, paths, save_path, add_gap_size):
    if meshes == None or len(meshes) == 0:
        print("No Meshes.")
        return
    nTotalCount = len(meshes)
    idx = 0
    while(True):
        sec_x_min_pos = meshes[idx].x.max() + add_gap_size
        gap_size = sec_x_min_pos - meshes[idx + 1].x.min()
        
        meshes[idx + 1].x = meshes[idx + 1].x + np.ones(meshes[idx + 1].x.shape) * gap_size
        if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
        idx += 1
        if idx > nTotalCount - 2:
            break
    if paths[idx].find('lower\\') > -1:
            meshes[idx].z = meshes[idx].z - 3
    
    brick_mesh = mesh.Mesh.from_file(brick_path)
    brick_z_dis = meshes[0].z.min() - brick_mesh.z.max()
    brick_x_dis = meshes[0].x.min() - brick_mesh.x.min()
    # brick_mesh.x = brick_mesh.x + np.ones(brick_mesh.x.shape) * brick_x_dis
    brick_mesh.z = brick_mesh.z + np.ones(brick_mesh.z.shape) * brick_z_dis
    
    letters_length = meshes[nTotalCount - 1].x.max() - meshes[0].x.min()
    brick_length = brick_mesh.x.max() - brick_mesh.x.min()
    brick_count = math.ceil(letters_length / brick_length)
    space_length = (brick_count * brick_length - letters_length) / 2
    brick_mesh.x = brick_mesh.x + np.ones(brick_mesh.x.shape) * brick_x_dis - np.ones(brick_mesh.x.shape) * space_length
    
    brick_idx = 0
    while brick_idx < brick_count:
        brick_idx_mesh = mesh.Mesh.from_file(brick_path)
        brick_idx_mesh.x = brick_mesh.x + np.ones(brick_idx_mesh.x.shape) * brick_length * brick_idx
        brick_idx_mesh.z = brick_mesh.z
        brick_idx += 1
        meshes.append(brick_idx_mesh)
    combine_stl(meshes, save_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Input word to get.")
        exit()

    strInput = sys.argv[1]
    
    direc = os.getcwd()
    filesSTL = []
    strOutPath = os.path.join(direc, strInput + '.stl')
    strBrickPath = os.path.join(direc, "mattoncino.stl")
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
        # combine_stl_horizontally(meshes, paths, strOutPath, 3)
        combine_stl_h_brick(meshes, strBrickPath, paths, strOutPath, 3)
        print('Output to ' + strOutPath + '\n')