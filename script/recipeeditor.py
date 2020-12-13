from tkinter import *
from tkinter.ttk import *
import pickle as pk
from .recipe import *
from .recipeeditordata import RecipeEditorData as Data
import os
from PIL import ImageTk, Image
from tkinter import filedialog
from shutil import copyfile
from ttkthemes import ThemedStyle, ThemedTk
import json
from more_itertools import pairwise


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
            self.currentRecipe = list(self.recipes.values())[0]
        except:
            self.recipes = Data().getRecipeDataWithBasicRecipe()
            fileRecipes = open(self.recipeDataFileName, 'w+')
            json.dump(self.recipes, fileRecipes)
            self.currentRecipe = list(self.recipes.values())[0]

    def createLayout(self):
        self.addMenuBar()
        self.addRecipeEditorLabel()
        self.addRecipeNameRow()
        self.addAuthorrow()
        self.addIndexTagsRow()
        self.addIngridientList()
        self.addSteps()
        self.addCookParameter()
        self.addPictureShow()
        self.addSearchForNewPictureButton()

    def addMenuBar(self):
        self.menubar = Menu(self.app)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Oeffne Rezept", command=self.addChooseRow)
        self.filemenu.add_command(
            label="Neues Rezept", command=self.addNewRecipe)
        self.filemenu.add_command(
            label="Rezept speichern", command=self.saveRecipe)
        self.filemenu.add_command(label="Rezept loeschen")
        self.filemenu.add_command(label="Exit", command=self.app.quit)

        self.exportmenu = Menu(self.menubar, tearoff=0)
        self.exportmenu.add_command(label="Export Rezept einzeln")
        self.exportmenu.add_command(label="Export Rezeptbuch")

        self.menubar.add_cascade(label="Rezept", menu=self.filemenu)
        self.menubar.add_cascade(label="Export", menu=self.exportmenu)
        self.app.config(menu=self.menubar)

    def addRecipeEditorLabel(self):
        self.app.title("Recipe Editor")

    def addChooseRow(self):
        self.selectRecipeWindow = Toplevel(self.app)
        self.addChooseLabel()
        self.addDropdownRecipeList()
        Button(self.selectRecipeWindow, text="Oeffne",
               command=self.chooseNewRecipe).grid(column=0, row=1)
        Button(self.selectRecipeWindow, text="Cancel",
               command=self.newRecipeWindow.destroy).grid(column=1, row=1)
        self.selectRecipeWindow.transient(self.app)
        self.selectRecipeWindow.grab_set()
        self.app.wait_window(self.selectRecipeWindow)

    def chooseNewRecipe(self):
        newRecipeTitle = self.recipeListVariable.get()
        self.currentRecipe = self.recipes.dict[newRecipeTitle]
        self.updateInput()
        self.selectRecipeWindow.destroy()

    def addChooseLabel(self):
        chooseLabel = Label(self.selectRecipeWindow, text="Waehle Rezept aus:")
        chooseLabel.grid(column=0, row=0)

    def addDropdownRecipeList(self):
        self.recipeListVariable = StringVar(self.selectRecipeWindow)
        self.recipeListVariable.set(list(self.recipes.keys())[0])

        self.recipeDropdown = OptionMenu(
            self.selectRecipeWindow, self.recipeListVariable, *self.recipes.list)
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
        self.recipes[newRecipeTitle] = getEmptyRecipeDict()
        self.currentRecipe = self.recipes[newRecipeTitle]
        self.updateInput()
        self.newRecipeWindow.destroy()

    def updateInput(self):
        return

    def addRecipeNameRow(self):
        chooseLabel = Label(self.app, text=" Rezeptname:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.recipeNameEntry = Entry(self.app, width=50)
        self.recipeNameEntry.grid(
            column=1, row=self.maxRow, columnspan=4, sticky="w")
        self.recipeNameEntry.insert(0, self.currentRecipe["recipeTitle"])
        self.maxRow += 1

    def addAuthorrow(self):
        chooseLabel = Label(self.app, text=" Autor:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.authorEntry = Entry(self.app, width=50)
        self.authorEntry.grid(column=1, row=self.maxRow,
                              columnspan=4, sticky="w")
        self.authorEntry.insert(0, self.currentRecipe["author"])
        self.maxRow += 1

    def addIndexTagsRow(self):
        chooseLabel = Label(self.app, text=" Stichwoerter:")
        chooseLabel.grid(column=0, row=self.maxRow, sticky="w")
        self.indexTagsEntry = Entry(self.app, width=50)
        self.indexTagsEntry.grid(
            column=1, row=self.maxRow, columnspan=4, sticky="w")
        self.indexTagsEntry.insert(
            0, ",".join(self.currentRecipe["indexTags"]))
        self.maxRow += 1

    def addIngridientList(self):
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
        self.ingridienttextbox.delete('1.0', END)
        ingridientstring = ""
        for ingreds in self.currentRecipe["ingredients"]:
            if ingreds != "" and ingreds != None:
                ingridientstring += ingreds+":\n"
            for ingridient in self.currentRecipe["ingredients"][ingreds]:
                ingridientstring += ingridient+"\n"
        self.ingridienttextbox.insert(END, ingridientstring)
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
        self.stepstextbox.delete('1.0', END)
        stepsstring = ""
        for step in self.currentRecipe["cookingSteps"]:
            stepsstring += step+"\n\n"
        self.stepstextbox.insert(END, stepsstring)
        self.maxRow += 4

    def saveRecipe(self):
        del self.recipes[self.currentRecipe["recipeTitle"]]
        self.currentRecipe["recipeTitle"] = self.recipeNameEntry.get()
        self.currentRecipe["author"] = self.authorEntry.get()
        self.currentRecipe["indexTags"] = [
            indexTag.strip() for indexTag in self.indexTagsEntry.get().split(",")]
        self.currentRecipe["prepTime"] = self.prepTimeEntry.get()
        self.currentRecipe["waitTime"] = self.waitTimeEntry.get()
        self.currentRecipe["portionSize"] = self.portionEntry.get()
        self.updateCurrenRecipeIngredients()
        self.updateCurrentRecipeMethod()
        self.recipes[self.currentRecipe["recipeTitle"]]=self.currentRecipe
        fileRecipes = open(self.recipeDataFileName, 'w+')
        json.dump(self.recipes, fileRecipes)
        self.updateInput()

    def updateCurrenRecipeIngredients(self):
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
                ingredientsKey = ingredientList[i].replace(":","").strip()
                startIndex = i+1
            ingredientPart = ingredientList[startIndex:
                                            j] if j != "End" else ingredientList[startIndex:]
            self.currentRecipe["ingredients"][ingredientsKey] = [
                x for x in ingredientPart if len(x) > 0]
        self.recipes[self.currentRecipe["recipeTitle"]] = self.currentRecipe

    def updateCurrentRecipeMethod(self):
        self.currentRecipe["cookingSteps"] = [
            x.strip() for x in self.stepstextbox.get("1.0", END).split("\n\n") if len(x.strip())!=0]
        

    def addExportRecipeButton(self):
        self.exportRecipeButton = Button(self.app,
                                         text="Export Recipe",
                                         command=self.exportAsPDFRecipe)
        self.exportRecipeButton.grid(column=5, row=6, columnspan=1)

    def exportAsPDFRecipe(self):
        # Todo
        return

    def addCookParameter(self):
        self.prepTimeLabel = Label(self.app, text="Zubereitungzeit (min): ")
        self.prepTimeLabel.grid(column=4, row=3, sticky='w', padx=5)
        self.waitTimeLabel = Label(self.app, text="Wartezeit (min): ")
        self.waitTimeLabel.grid(column=4, row=4, sticky='w', padx=5)
        self.portionLabel = Label(self.app, text="Portionen: ")
        self.portionLabel.grid(column=4, row=5, sticky='w', padx=5)
        self.prepTimeEntry = Entry(self.app)
        self.prepTimeEntry.grid(column=5, row=3)
        self.prepTimeEntry.insert(0, self.currentRecipe["prepTime"])
        self.waitTimeEntry = Entry(self.app)
        self.waitTimeEntry.grid(column=5, row=4)
        self.waitTimeEntry.insert(0, self.currentRecipe["waitTime"])
        self.portionEntry = Entry(self.app)
        self.portionEntry.grid(column=5, row=5)
        self.portionEntry.insert(0, self.currentRecipe["portionSize"])

    def addPictureShow(self):
        pictureFilePath = os.path.join(
            os.getcwd(), self.currentRecipe["pictureFile"])
        self.setNewPictureImg(pictureFilePath)
        self.pictureLabel = Label(self.app, image=self.img)
        self.pictureLabel.grid(column=4, row=6,
                               columnspan=2, pady=30, padx=30, rowspan=4)
        self.maxRow += 1

    def setNewPictureImg(self, pictureFilePath):
        self.img1 = Image.open(pictureFilePath)
        self.img1 = self.img1.resize((200, 200), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img1)

    def addSearchForNewPictureButton(self):
        self.newPictureButton = Button(self.app,
                                       text="Neues Bild laden",
                                       command=self.getNewPicutre)
        self.newPictureButton.grid(column=4, row=10, columnspan=2)

    def getNewPicutre(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="Waehle Bild aus")
        newFilePos = os.path.join(os.path.join(
            os.getcwd(), "pictures"), os.path.split(filename)[1])
        copyfile(filename, newFilePos)
        self.currentRecipe["pictureFile"] = os.path.split(filename)[1]
        self.setNewPictureImg(newFilePos)
        self.pictureLabel.configure(image=self.img)
