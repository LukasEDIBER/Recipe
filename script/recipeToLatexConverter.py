# -*- coding: utf-8 -*-
from pathlib import Path
import os


class RecipeToLatexConverter:

    umlautDict = {"Ä": "{\"A}", "Ö": "{\"O}", "Ü": "{\"U}",
                  "ä": "{\"a}", "ö": "{\"o}", "ü": "{\"u}",
                  "ß": "{\ss}", "&": "\&", "°": "$^{\circ}$",
                  "º": "$^{\circ}$", "á":"\' a"}

    def __init__(self, texFolder: str):

        self.recipeFolder = texFolder
        print(self.recipeFolder)

    def setRecipe(self, recipe: dict):
        self.recipe = recipe
        self.recipeName = recipe["recipeTitle"].lower().replace(" ", "")
        self.convertUmlaute()

    def convertUmlauteForLatexString(self, inputString: str):
        for umlaut in self.umlautDict:
            inputString = inputString.replace(umlaut, self.umlautDict[umlaut])
        return inputString

    def convertUmlaute(self):
        for key in ["recipeTitle", "portionSize", "author"]:
            self.recipe[key] = self.convertUmlauteForLatexString(
                self.recipe[key])
        newTags = []
        for tag in self.recipe["indexTags"]:
            newTags.append(self.convertUmlauteForLatexString(tag))
        self.recipe["indexTags"] = newTags
        newIngred = {}
        for ingredHeader in self.recipe["ingredients"]:
            newIngredHeader = self.convertUmlauteForLatexString(ingredHeader)
            print(newIngredHeader)
            newIngred[newIngredHeader] = []
            for ingreds in self.recipe["ingredients"][ingredHeader]:
                print(ingreds)
                newIngred[newIngredHeader].append(
                    self.convertUmlauteForLatexString(ingreds))
        self.recipe["ingredients"] = newIngred
        newCookingSteps = []
        for cookingStep in self.recipe["cookingSteps"]:
            newCookingSteps.append(
                self.convertUmlauteForLatexString(cookingStep))
        self.recipe["cookingSteps"] = newCookingSteps

    def writeLatexFile(self):
        with open(os.path.join(self.recipeFolder, self.recipeName+'.tex'), 'w+') as self.texFile:
            self.writeRecipeHeader()
            self.writePrepInfo()
            self.writeIngrendientsAndPicture()
            self.writeSteps()

    def writeSingleRecipeLatexFile(self, recipe: dict):
        self.setRecipe(recipe)
        with open(os.path.join(self.recipeFolder, self.recipeName+'.tex'), 'w+') as self.texFile:
            self.writeDocumentClass()
            self.writeStyleFile()
            self.writeDocumentBegin()
            self.writeRecipeHeader()
            self.writePrepInfo()
            self.writeIngrendientsAndPicture()
            self.writeSteps()
            self.writeDocumentEnd()
        return os.path.join(self.recipeFolder, self.recipeName+'.tex')

    def writeDocumentClass(self):
        self.texFile.write("\\documentclass{article}\n")

    def writeStyleFile(self):
        print(os.getcwd())
        with open(os.path.join(os.getcwd(), "tex", "stylefile.tex"), 'r+') as file:
            styleString = file.read()
            self.texFile.write(styleString)
            self.texFile.write("\n")

    def writeDocumentBegin(self):
        self.texFile.write("\\begin{document}\n")
        self.texFile.write("\\setcounter{secnumdepth}{-2}")

    def writeDocumentEnd(self):
        self.texFile.write("\\end{document}\n")

    def writeRecipeHeader(self):
        recipeHeader = "\\recipe["
        if self.recipe["author"] is not None:
            recipeHeader += "by "+self.recipe["author"]
        for indexTag in self.recipe["indexTags"]:
            recipeHeader += "\\index{"+indexTag+"}"
        recipeHeader += "]{"+self.recipe["recipeTitle"]+"}\n"
        self.texFile.write(recipeHeader)

    def writePrepInfo(self):
        prepInfo = "\\footnotesize{"
        prepInfo += ""+str(self.recipe["portionSize"])+", "
        prepInfo += "Zubereitungszeit: " + \
            str(self.recipe["prepTime"]) + " Minuten, "
        prepInfo += "Wartezeit: "+str(self.recipe["waitTime"]) + " Minuten "
        prepInfo += "}\n\\small"
        self.texFile.write(prepInfo)
        self.writeEmptyLine()

    def writeEmptyLine(self):
        self.texFile.write("\\\\\n")

    def writeIngrendientsAndPicture(self):
        ingreds = "\\begin{ingreds}\n"
        for ingredsKey in self.recipe["ingredients"]:
            if ingredsKey != "" and ingredsKey != None:
                ingreds += "\\ingredients["+ingredsKey+":]\n"
            for ingrediant in self.recipe["ingredients"][ingredsKey]:
                ingreds += ingrediant+"\n"
        if self.recipe["pictureFile"] != None and self.recipe["pictureFile"] != "":
            ingreds += "\\columnbreak\n"
            ingreds += "\\showit[1in]{"+self.recipe["pictureFile"]+"}\n"
        ingreds += "\\end{ingreds}\n"
        self.texFile.write(ingreds)

    def writeSteps(self):
        steps = "\\begin{method}\n"
        for step in self.recipe["cookingSteps"]:
            steps += "\n"+step+"\n"
        steps += "\\end{method}\n"
        self.texFile.write(steps)
