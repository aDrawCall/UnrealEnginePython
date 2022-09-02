import tkinter
from turtle import bgcolor
import unreal

from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
import os
from os import listdir 
from os.path import isfile, join 



#Global Variables 
importDIR = str("empty")
unrealDir = r'/Game/BradsTestMeshes'

#Unreal Importing Setup
AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
unrealImportTasks = []


# This function looks at the global directory that is set 
def ImportIntoUnreal():
    global unrealImportTasks
    global unrealDir
    for fbxFilePath in grabAllFbxFilePaths():
        AssetImportTask = unreal.AssetImportTask()
        AssetImportTask.set_editor_property('replace_existing', True)
        AssetImportTask.set_editor_property('replace_existing_settings', False)
        AssetImportTask.set_editor_property('automated', True)
        AssetImportTask.set_editor_property('filename', fbxFilePath)
        AssetImportTask.set_editor_property('destination_path', unrealDir)
        AssetImportTask.set_editor_property('save', False)
        unrealImportTasks.append(AssetImportTask)
    
        
    
    AssetTools.import_asset_tasks(unrealImportTasks)
    print("Imported Into Unreal Finished")
    #Exit the program  by destroying the tkinter window when its done. 
    root.destroy()
    
    


  
 #Gets a list of all the files inside of the sub directories of our main "importDIR" returned as full paths  
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles    

def grabAllFbxFilePaths():
    files = getListOfFiles(importDIR)
    fbxlist = list()
    for file in files:
        if file[-3:] == "fbx": 
            fbxlist.append(file)
            
    return fbxlist
               
    
def setUnrealDir():
    global unrealDir
    global strUnrealDir
    unrealDir = strUnrealDir.get()
    
    print(unrealDir)      

#This opens a file section window and then sets a global variable to that directory path, we can then do things with this file path    
def fileDialogSelection():
    folder_selected = filedialog.askdirectory()
    label = ttk.Label(mainframe, text= folder_selected).grid(column=1, row=4, sticky=W)
    global importDIR
    importDIR = folder_selected

#This is the GUI Setup 
root = Tk()
root.title("Brads UE4 FBX Asset Importer")
mainframe = ttk.Frame(root, padding="12 12 24 24")
mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
root.columnconfigure(0, weight=12)
root.rowconfigure(0, weight=12)


#These are the main GUI buttons for selecting the directory and then importing the files from that directory
strUnrealDir = tkinter.StringVar()
e = ttk.Entry (mainframe, textvariable=strUnrealDir).grid(column=1, row = 2, sticky = W)
unrealDir = strUnrealDir.get()
ttk.Button(mainframe, text="Unreal Install Directory",command=setUnrealDir).grid(column=2, row = 2, sticky = W)
ttk.Label(mainframe, text=strUnrealDir.get()).grid(column=3,row=2)
root.bind('<Return>', setUnrealDir())

ttk.Button(mainframe, text="Art Source Directory",command=fileDialogSelection).grid(column=2, row = 4, sticky = W)
ttk.Button(mainframe, text="IMPORT", command=ImportIntoUnreal).grid(column=4, row = 4, sticky = W)


#Gui Update Loop 
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
root.mainloop()


