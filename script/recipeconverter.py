# -*- coding: utf-8 -*-
from pathlib import Path


class RecipeConverter:
    def __init__(self, recipe: dict, texFolder: str):
        self.recipe = recipe
        self.recipeName = +recipe["recipeTitle"].lower().replace(" ", "")
        self.recipeFolder = texFolder
        print(self.recipeFolder)

    def writeLatexFile(self):
        with open(self.recipeFolder+'/'+self.recipeName+'.tex', 'w+') as self.texFile:
            self.writeRecipeHeader()
            self.writePrepInfo()
            self.writeIngrendientsAndPicture()
            self.writeSteps()

    def writeRecipeHeader(self):
        recipeHeader = "\\recipe["
        if self.recipe["author"] is not None:
            recipeHeader += "by "+self.recipe["author"]
        for indexTag in self.recipe["indexTags"]:
            recipeHeader += "\\index{"+indexTag+"}"
        recipeHeader += "]{"+self.recipe["recipeTitle"]+"}\n"
        self.texFile.write(recipeHeader)

    def writePrepInfo(self):
        prepInfo = "\\small{"
        prepInfo += "Zubereitungszeit: " + \
            str(self.recipe["prepTime"]) + " Minuten "
        prepInfo += "Wartezeit: "+str(self.recipe["waitTime"]) + " Minuten "
        prepInfo += "Portionen: "+str(self.recipe["portionSize"])
        prepInfo += "}\n"
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
        if self.recipe["pictureFile"] != None:
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


if __name__ == "__main__":
    recipe1 = Recipe()
    recipe1.recipeTitle = "Vegan Text"
    recipe1.indexTags = ["Test", "Best"]
    recipe1.author = "Lukas"
    recipe1.cookingSteps = ["1", "2"]
    recipe1.waitTime = 60
    recipe1.prepTime = 30
    recipe1.ingredients = {"Teig": ["100g Mehr", "200g More"]}
    recipe1.portionSize = "30 Kekse"
    recipe1.pictureFile = "vegantext.jpg"
    converter = RecipeConverter(recipe1)
    converter.writeLatexFile()
