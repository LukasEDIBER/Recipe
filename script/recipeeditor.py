from tkinter import *
from tkinter.ttk import *
import pickle as pk
import os
from PIL import ImageTk, Image
from tkinter import filedialog
from ttkthemes import ThemedStyle, ThemedTk
import json
import shutil
from shutil import copyfile
import subprocess
from more_itertools import pairwise
from .recipe import getRecipeDataWithBasicRecipe, getEmptyRecipeDict
from .recipeexporter import RecipeExport
import copy

class RecipeEditor:

    recipeDataFileName = "recipeData.json"
    maxRow = 0

    def __init__(self):
        self.loadRecipeData()
        self.app = ThemedTk(theme="yaru")
        self.app.configure(bg='white')
        self.createLayout()
        self.app.mainloop()

    def loadRecipeData(self):
        try:
            with open(self.recipeDataFileName, "r") as recipeDataJson:
                self.recipes = json.load(recipeDataJson)
            self.currentRecipe = self.recipes[sorted(
                list(self.recipes.keys()))[0]]
        except:
            self.recipes = getRecipeDataWithBasicRecipe()
            self.saveToJson()
            self.currentRecipe = list(self.recipes.values())[0]
        self.initCategories()

    def initCategories(self):
        self.categorySet=set()
        for recipe in self.recipes.values():
            self.categorySet.add(recipe["category"])
        print(self.categorySet)

    def createLayout(self):
        self.addMenuBar()
        self.setAppTitle()
        self.addRecipeNameWidgets()
        self.addAuthorWidgets()
        self.addCatercoryWidgets()
        self.addIndexTagsWidgets()
        self.addIngridientWidgets()
        self.addSteps()
        self.addCookParameterWidgets()
        self.addPictureShow()
        self.addSearchForNewPictureButton()
        self.updateInput()

    def addMenuBar(self):
        self.menubar = Menu(self.app)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Öffne Rezept", command=self.chooseNewRecipeWindow, accelerator="Ctrl+O")
        self.app.bind(
            "<Control-o>", lambda event: self.chooseNewRecipeWindow())
        self.filemenu.add_command(
            label="Neues Rezept", command=self.addNewRecipe, accelerator="Ctrl+N")
        self.app.bind("<Control-n>", lambda event: self.addNewRecipe())
        self.filemenu.add_command(
            label="Rezept speichern", command=self.saveRecipe, accelerator="Ctrl+S")
        self.app.bind("<Control-s>", lambda event: self.saveRecipe())
        self.filemenu.add_command(
            label="Rezept löschen", command=self.openDeleteRecipeWindow, accelerator="Ctrl+D")
        self.app.bind(
            "<Control-d>", lambda event: self.openDeleteRecipeWindow())
        self.filemenu.add_command(label="Exit", command=self.app.quit)

        self.exportmenu = Menu(self.menubar, tearoff=0)
        self.exportmenu.add_command(
            label="Export Rezept einzeln", command=self.exportSingleLatex)
        self.exportmenu.add_command(
            label="Export Rezeptbuch", command=self.exportBookletLatex)

        self.menubar.add_cascade(label="Rezept", menu=self.filemenu)
        self.menubar.add_cascade(label="Export", menu=self.exportmenu)
        self.app.config(menu=self.menubar)

    def exportSingleLatex(self):
        RecipeExport().exportSingleRecipe(copy.deepcopy(self.currentRecipe))

    def exportBookletLatex(self):
        RecipeExport().exportBookletLatex(copy.deepcopy(self.recipes))

    def setAppTitle(self):
        self.app.title("Recipe Editor")

    def chooseNewRecipeWindow(self):
        self.selectRecipeWindow = Toplevel(self.app)
        self.addChooseRecipeLabel(self.selectRecipeWindow)
        self.addDropdownWidgetRecipeListTo(self.selectRecipeWindow)
        Button(self.selectRecipeWindow, text="Öffne",
               command=self.openNewRecipe).grid(column=0, row=1)
        Button(self.selectRecipeWindow, text="Cancel",
               command=self.selectRecipeWindow.destroy).grid(column=1, row=1)
        self.selectRecipeWindow.transient(self.app)
        self.selectRecipeWindow.grab_set()
        self.app.wait_window(self.selectRecipeWindow)

    def openNewRecipe(self):
        newRecipeTitle = self.recipeListVariable.get()
        self.currentRecipe = self.recipes[newRecipeTitle]
        self.updateInput()
        self.selectRecipeWindow.destroy()

    def addChooseRecipeLabel(self, windowWidget):
        chooseLabel = Label(windowWidget, text="Wähle Rezept aus:")
        chooseLabel.grid(column=0, row=0)

    def addDropdownWidgetRecipeListTo(self, windowWidget):
        self.recipeTitles = sorted(list(self.recipes.keys()))
        self.recipeListVariable = StringVar(windowWidget)
        self.recipeListVariable.set(self.currentRecipe["recipeTitle"])

        self.recipeDropdown = OptionMenu(
            windowWidget, self.recipeListVariable, self.currentRecipe["recipeTitle"], *self.recipeTitles)
        self.recipeDropdown.grid(column=1, row=0, sticky="W")

    def addNewRecipe(self):
        self.newRecipeWindow = Toplevel(self.app)
        Label(self.newRecipeWindow, text="Recipe title: ").grid(
            column=0, row=0)
        self.recipeTitleEnty = Entry(self.newRecipeWindow)
        self.recipeTitleEnty.grid(column=1, row=0)
        Button(self.newRecipeWindow, text="Add",
               command=self.addNewRecipeFromEntry).grid(column=0, row=1)
        Button(self.newRecipeWindow, text="Cancel",
               command=self.newRecipeWindow.destroy).grid(column=1, row=1)
        self.newRecipeWindow.transient(self.app)
        self.newRecipeWindow.grab_set()
        self.app.wait_window(self.newRecipeWindow)

    def addNewRecipeFromEntry(self):
        newRecipeTitle = self.recipeTitleEnty.get()
        if newRecipeTitle == "" or newRecipeTitle == None:
            return
        if newRecipeTitle in self.recipes.keys():
            self.currentRecipe = self.recipes[newRecipeTitle]
            self.updateInput()
            return
        self.recipes[newRecipeTitle] = getEmptyRecipeDict(newRecipeTitle)
        self.currentRecipe = self.recipes[newRecipeTitle]
        self.currentRecipe = self.getNewIdNr()
        self.saveRecipe()
        self.updateInput()
        self.newRecipeWindow.destroy()

    def getNewIdNr(self):
        out = 0
        for recipe in self.recipes.values():
            out = max(out, recipe["id"])
        return out+1

    def updateInput(self):
        self.updateRecipeName()
        self.updateAuthorName()
        self.updateIndexTags()
        self.updateCategory()
        self.updateIngredients()
        self.updateSteps()
        self.updateCookParameters()
        self.updatePicture()

    def updateRecipeName(self):
        self.recipeNameEntry.delete(0, 'end')
        self.recipeNameEntry.insert(0, self.currentRecipe["recipeTitle"])

    def updateAuthorName(self):
        self.authorEntry.delete(0, 'end')
        self.authorEntry.insert(0, self.currentRecipe["author"])

    def updateIndexTags(self):
        self.indexTagsEntry.delete(0, 'end')
        self.indexTagsEntry.insert(
            0, ",".join(self.currentRecipe["indexTags"]))

    def updateCategory(self):
        self.categoryVariable.set(self.currentRecipe["category"])
        self.categoryDropdown = OptionMenu(
            self.app, self.categoryVariable, self.currentRecipe["category"], *self.categorySet)

    def updateIngredients(self):
        self.ingridienttextbox.delete('1.0', END)
        ingridientstring = ""
        for ingreds in self.currentRecipe["ingredients"]:
            if ingreds != "" and ingreds != None:
                ingridientstring += ingreds+":\n"
            for ingridient in self.currentRecipe["ingredients"][ingreds]:
                ingridientstring += ingridient+"\n"
        self.ingridienttextbox.insert(END, ingridientstring)

    def updateSteps(self):
        self.stepstextbox.delete('1.0', END)
        stepsstring = ""
        for step in self.currentRecipe["cookingSteps"]:
            stepsstring += step+"\n\n"
        self.stepstextbox.insert(END, stepsstring)

    def updateCookParameters(self):
        self.waitTimeEntry.delete(0, 'end')
        self.prepTimeEntry.delete(0, 'end')
        self.portionEntry.delete(0, 'end')
        self.waitTimeEntry.insert(0, self.currentRecipe["waitTime"])
        self.prepTimeEntry.insert(0, self.currentRecipe["prepTime"])
        self.portionEntry.insert(0, self.currentRecipe["portionSize"])

    def updatePicture(self):
        pictureFilePath = os.path.join(
            os.getcwd(), self.currentRecipe["pictureFile"])
        if os.path.exists(pictureFilePath) and os.path.isfile(pictureFilePath):
            self.updatePictureImg(pictureFilePath)
            self.pictureLabel.config(image=self.img)
        else:
            self.pictureLabel.config(image='')

    def updatePictureImg(self, pictureFilePath):
        self.img1 = Image.open(pictureFilePath)
        self.img1 = self.img1.resize((200, 200), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img1)

    def addRecipeNameWidgets(self):
        chooseLabel = Label(self.app, text=" Rezeptname:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.recipeNameEntry = Entry(self.app, width=50)
        self.recipeNameEntry.grid(
            column=1, row=self.maxRow, columnspan=4, sticky="w")
        self.maxRow += 1

    def addAuthorWidgets(self):
        authorLabel = Label(self.app, text=" Autor:")
        authorLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.authorEntry = Entry(self.app, width=50)
        self.authorEntry.grid(column=1, row=self.maxRow,
                              columnspan=4, sticky="w")
        self.maxRow += 1

    def addIndexTagsWidgets(self):
        chooseLabel = Label(self.app, text=" Stichwörter:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.indexTagsEntry = Entry(self.app, width=50)
        self.indexTagsEntry.grid(
            column=1, row=self.maxRow, columnspan=4, sticky="w")

        self.maxRow += 1

    def addCatercoryWidgets(self):
        chooseLabel = Label(self.app, text=" Kategorie:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.categoryVariable = StringVar(self.app)
        self.categoryVariable.set(self.currentRecipe["category"])
        self.categoryDropdown = OptionMenu(
            self.app, self.categoryVariable, self.currentRecipe["category"], *self.categorySet)
        self.categoryDropdown.grid(column=1, row=self.maxRow, columnspan=4, sticky="w")
        self.maxRow += 1

    def addIngridientWidgets(self):
        self.zutatenLabel = Label(self.app, text="Zutaten:")
        self.zutatenLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.maxRow += 1
        self.ingridienttextbox = Text(self.app, height=8, width=50)
        self.ingridientscrollbar = Scrollbar(
            self.app, orient="vertical", command=self.ingridienttextbox.yview,)
        self.ingridientscrollbar.grid(
            column=3, row=self.maxRow, sticky='nsw', rowspan=3)
        self.ingridienttextbox.grid(
            column=0, row=self.maxRow, columnspan=3, rowspan=3)
        self.ingridienttextbox.config(
            yscrollcommand=self.ingridientscrollbar.set)
        self.maxRow += 3

    def addSteps(self):
        self.zubereitunglabel = Label(self.app, text="Zubereitung:")
        self.zubereitunglabel.grid(column=0, row=self.maxRow, sticky="w")
        self.maxRow += 1
        self.stepstextbox = Text(self.app, height=12, width=50)
        self.stepsscrollbar = Scrollbar(
            self.app, orient="vertical", command=self.stepstextbox.yview,)
        self.stepsscrollbar.grid(
            column=3, row=self.maxRow, sticky='nsw', rowspan=4)
        self.stepstextbox.grid(column=0, row=self.maxRow,
                               columnspan=3, rowspan=4)
        self.stepstextbox.config(
            yscrollcommand=self.stepsscrollbar.set)
        self.maxRow += 4

    def addCookParameterWidgets(self):
        self.prepTimeLabel = Label(self.app, text="Zubereitungzeit (min): ")
        self.prepTimeLabel.grid(column=4, row=4, sticky='w', padx=5)
        self.waitTimeLabel = Label(self.app, text="Wartezeit (min): ")
        self.waitTimeLabel.grid(column=4, row=5, sticky='w', padx=5)
        self.portionLabel = Label(self.app, text="Portionen: ")
        self.portionLabel.grid(column=4, row=6, sticky='w', padx=5)
        self.prepTimeEntry = Entry(self.app)
        self.prepTimeEntry.grid(column=5, row=4)
        self.waitTimeEntry = Entry(self.app)
        self.waitTimeEntry.grid(column=5, row=5)
        self.portionEntry = Entry(self.app)
        self.portionEntry.grid(column=5, row=6)

    def addPictureShow(self):
        self.pictureLabel = Label(self.app)
        self.pictureLabel.grid(column=4, row=7,
                               columnspan=2, pady=30, padx=30, rowspan=4)
        self.maxRow += 1

    def addSearchForNewPictureButton(self):
        self.newPictureButton = Button(self.app,
                                       text="Neues Bild laden",
                                       command=self.getNewPicutre)
        self.newPictureButton.grid(column=4, row=11, columnspan=2)

    def getNewPicutre(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="Wähle Bild aus")
        newFilePos = os.path.join(os.path.join(
            os.getcwd(), "pictures"), os.path.split(filename)[1])
        if not os.path.isfile(newFilePos):
            copyfile(filename, newFilePos)
        else:
            print("Picture name already exists in database. Please change name!")
        self.currentRecipe["pictureFile"] = os.path.join(
            "pictures", os.path.split(filename)[1])
        self.updatePicture()

    def saveRecipe(self):
        if self.currentRecipe["recipeTitle"] in self.recipes:
            del self.recipes[self.currentRecipe["recipeTitle"]]
        self.currentRecipe["recipeTitle"] = self.recipeNameEntry.get()
        self.currentRecipe["author"] = self.authorEntry.get()
        self.currentRecipe["indexTags"] = [
            indexTag.strip() for indexTag in self.indexTagsEntry.get().split(",")]
        self.currentRecipe["prepTime"] = self.prepTimeEntry.get()
        self.currentRecipe["waitTime"] = self.waitTimeEntry.get()
        self.currentRecipe["portionSize"] = self.portionEntry.get()
        self.currentRecipe["category"] = self.categoryVariable.get()
        self.saveCurrenRecipeIngredients()
        self.saveCurrentRecipeMethod()
        self.recipes[self.currentRecipe["recipeTitle"]] = self.currentRecipe
        self.saveToJson()
        self.updateInput()

    def saveToJson(self):
        fileRecipes = open(self.recipeDataFileName, 'w+')
        json.dump(self.recipes, fileRecipes)

    def saveCurrenRecipeIngredients(self):
        self.currentRecipe["ingredients"].clear()
        ingredientList = [
            x.strip() for x in self.ingridienttextbox.get("1.0", END).split("\n")]
        headerLines = [i for i, x in enumerate(ingredientList) if ":" in x]
        headerLines = ["Start"]+headerLines+["End"]
        for i, j in pairwise(headerLines):
            ingredientsKey = ""
            startIndex = 0
            if i == "Start" and j == 0:
                continue
            if i != "Start":
                ingredientsKey = ingredientList[i].replace(":", "").strip()
                startIndex = i+1
            ingredientPart = ingredientList[startIndex:
                                            j] if j != "End" else ingredientList[startIndex:]
            self.currentRecipe["ingredients"][ingredientsKey] = [
                x for x in ingredientPart if len(x) > 0]
        self.recipes[self.currentRecipe["recipeTitle"]] = self.currentRecipe

    def saveCurrentRecipeMethod(self):
        self.currentRecipe["cookingSteps"] = [
            x.strip() for x in self.stepstextbox.get("1.0", END).split("\n\n") if len(x.strip()) != 0]

    def openDeleteRecipeWindow(self):
        self.selectRecipeWindow = Toplevel(self.app)
        self.addChooseRecipeLabel(self.selectRecipeWindow)
        self.addDropdownWidgetRecipeListTo(self.selectRecipeWindow)
        Button(self.selectRecipeWindow, text="Delete",
               command=self.deleteRecipe).grid(column=0, row=1)
        Button(self.selectRecipeWindow, text="Cancel",
               command=self.selectRecipeWindow.destroy).grid(column=1, row=1)
        self.selectRecipeWindow.transient(self.app)
        self.selectRecipeWindow.grab_set()
        self.app.wait_window(self.selectRecipeWindow)

    def deleteRecipe(self):
        toDeleteRecipeTitle = self.recipeListVariable.get()
        del self.recipes[toDeleteRecipeTitle]
        if toDeleteRecipeTitle == self.currentRecipe["recipeTitle"]:
            self.currentRecipe = list(self.recipes.values())[0]
            self.updateInput()
        self.saveToJson()
        self.selectRecipeWindow.destroy()
