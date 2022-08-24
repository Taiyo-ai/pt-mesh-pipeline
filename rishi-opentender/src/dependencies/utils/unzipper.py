import zipfile
import os
from typing import List


class unzip:
    def __init__(self, filename: List[str], path):
        self.file = filename
        self.path = path

    def isFileExist(self, i):
        return os.path.isfile(os.path.join(self.path, i))

    def makefileDir(self, i):
        if self.isFileExist(i):
            try:
                os.mkdir(os.path.join(self.path, i))
                return True
            except FileExistsError:
                print(f"{i} directory already exist in {self.path}")
                return True
        else:
            print(f"Please Make {i} already exist in the {self.path} directory.")
            return False

    def extract(self):
        for i in self.file:
            file = i
            filename, fileext = i.split(".")
            if self.isFileExist(file) and self.makefileDir(file):
                try:
                    with zipfile.ZipFile(os.path.join(self.path, file), "r") as z:
                        z.extractall(os.path.join(self.path, filename))
                        print("Extracting... Done")
                except Exception as e:
                    print("Error while extracting : ", e)


"""
def unzqip(file):
    back = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    path = os.path.join(back, 'data')
    if (os.path.isfile(os.path.join(path,file))):
        with zipfile.ZipFile(os.path.join(path,file), 'r') as z:
            if (os.path.isdir(os.mkdir(os.path.join(path,file.split('.')[0])))) :
            # else :
                os.mkdir(os.path.join(path, file.split('.')[0]))
            print(f'Extracting... {file}')
            z.extractall(os.path.join(path, file.split('.')[0]))
            print(os.path.join(path,file.split('.')[0]))
            return(os.path.join(path,file.split('.')[0]))
"""
