import os
import sys
import shutil

rootDir = 'C:\\' # Windows

# define the file that will be converted to .exe
fileName = 'my_test_file.py'

# define the file path of the file that will be converted.
# default value is current working directory or cwd (pwd)
filePath = os.getcwd()
# where cxfreeze is installed on your local machine
# This might be in C:\\python36\Scripts\cxfreeze
# cxfreeze is not a path but the cxfreeze library
cxFreezePath = os.path.join(rootDir, "venv", "Scripts", "cxfreeze")

if os.path.isdir(filePath):
    if os.path.isfile(os.path.join(filePath, fileName)):
        # define python3 cxfreeze file path
        path = cxFreezePath
        # Run python process of converting .py to .exe
        os.system("python " + path + " " + os.path.join(filePath, fileName))
        # copy all files in add-to-root/dll-files/ into the dist folder
    else:
        print("File: {} not found.".format(fileName))
else:
    print("Directory: {} not found.".format(filePath))


# copy files from the folders in directory "add-to-root" into the "dist" directory once it is created
addToRootPath = os.path.join(os.getcwd(), 'firststreet')

for folderName in os.listdir(addToRootPath):
    for fileName in os.listdir(os.path.join(addToRootPath, folderName)):
        shutil.copy(os.path.join(addToRootPath, folderName, fileName), os.path.join(os.getcwd(), 'dist', fileName))
