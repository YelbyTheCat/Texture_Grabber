import bpy
import bmesh
import glob
import shutil
import os
from pathlib import Path

def run():
    #Check File
    path = bpy.path.abspath("//")
    path += "Textures"
    isFile = os.path.isdir(path)
    if not isFile:
        os.makedirs(path)
        print("Texture Folder Created")
    else:
        print("Texture Directory Already Exists")
    
    #Get the selected object
    obj = bpy.context.object

    #Get materials
    materials = obj.data.materials
    texture_list = []
    materialSlots = obj.material_slots

    for mat in materialSlots:
        print("~~Material: " + mat.name)
        if mat.material and mat.material.use_nodes:
            for texture in mat.material.node_tree.nodes:
                if texture.type == 'TEX_IMAGE':
                    #Get Image
                    tex = bpy.data.images[texture.image.name]
                    full_path = bpy.path.abspath(tex.filepath, library=tex.library)
                    norm_path = os.path.normpath(full_path)
                    #Fix
                    fixedName = str(cleanName(os.path.splitext(texture.image.name)))
                    #print("~Texture Name: " + fixedName)
                    #Location
                    newLocation = path + '\\' + fixedName
                    #print("Current Location: " + norm_path)
                    #print("New Location: " + newLocation)
                    
                    if os.path.isfile(norm_path) and not os.path.isfile(newLocation):
                        #print("Mat: " + mat.name + " | uses: " + texture.image.name + " Location: " + texture.image.filepath)
                        newLocation = path + '\\' + mat.name + " - " + fixedName
                        print(newLocation)
                        
                        #Copy
                        shutil.copy(norm_path, newLocation)
                        texture.image = bpy.data.images.load(newLocation)
                        print("Image Copied: " + fixedName)
                    elif os.path.isfile(norm_path) and os.path.isfile(newLocation):
                        print("Already Exists: " + fixedName)
                    else:
                        print("File Missing: " + fixedName)
                    print("")
        

def cleanName(fileName):
    fileTypes = [".png",".jpg",".jpeg",".psd",".bmp",".gif",".dds",".tif",".tiff"]
    for extention in fileTypes:
        if fileName[1] == extention:
            name = fileName[0] + fileName[1]
            return name
    name = os.path.splitext(fileName[0])
    return cleanName(name)
        

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

if __name__ == "__main__":
    print("~~~START OF CODE~~~")
    run()
    print("~~~END OF CODE~~~")