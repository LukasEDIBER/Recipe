import os
from .recipeToLatexConverter import RecipeToLatexConverter
from tkinter import filedialog
import shutil
from shutil import copyfile
import subprocess


class RecipeExport:
    def __init__(self):
        return

    def exportSingleRecipe(self, recipe: dict):
        self.recipeToWrite = recipe.copy()
        self.setPdfFolderLocation()
        self.createTexFolder(self.recipeToWrite["recipeTitle"])
        self.copyPictureToTexFolder()

        self.texfile = RecipeToLatexConverter(
            self.latexFolder).writeSingleRecipeLatexFile(self.recipeToWrite)
        self.runLatex()
        self.copyPdfToLocation()
        shutil.rmtree(self.latexFolder, ignore_errors=True)

    def setPdfFolderLocation(self):
        self.pdfFileDirectory = filedialog.askdirectory(
            initialdir="/", title="Waehle Ordner")

    def createTexFolder(self, folderName: str):
        texFolderName = folderName.lower().replace(
            " ", "")
        self.latexFolder = os.path.join(os.getcwd(), "tex", texFolderName)
        try:
            if not os.path.exists(self.latexFolder):
                os.makedirs(self.latexFolder)
        except Exception as e:
            print(e)
            print("Cannot create Folder at "+os.getcwd())

    def copyPictureToTexFolder(self):
        newPicturePos = ""
        if self.recipeToWrite["pictureFile"] != "":
            oldPicturePos = os.path.join(
                os.getcwd(), self.recipeToWrite["pictureFile"])
            newPicturePos = os.path.join(
                self.latexFolder, os.path.split(oldPicturePos)[1])
            if not os.path.isfile(newPicturePos):
                try:
                    copyfile(oldPicturePos, newPicturePos)
                except:
                    print("Picture "+oldPicturePos +
                          " cannot be found or copied. No Picture is used")
                    newPicturePos = ""
            self.recipeToWrite["pictureFile"] = newPicturePos.replace(
                "\\", "/")

    def runLatex(self):
        subprocess.run(
            ["pdflatex", self.texfile, "-output-directory="+os.path.split(self.texfile)[0]])

    def copyPdfToLocation(self):
        copyfile(self.texfile.replace(".tex", ".pdf"), os.path.join(
            self.pdfFileDirectory, os.path.split(self.texfile)[1].replace(".tex", ".pdf")))
