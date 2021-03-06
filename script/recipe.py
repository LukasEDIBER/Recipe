from collections import UserDict


def getEmptyRecipeDict(recipeTitle: str):
    out = {}
    out["recipeTitle"] = recipeTitle
    out["indexTags"] = []
    out["prepTime"] = ""
    out["waitTime"] = ""
    out["portionSize"] = ""
    out["ingredients"] = {}
    out["pictureFile"] = ""
    out["cookingSteps"] = []
    out["author"] = ""
    out["category"] = "Allgemein"
    out["id"] = 0
    return out


def getRecipeDataWithBasicRecipe():
    recipe1 = getEmptyRecipeDict("Vegane cremige Brokkoli Sosse")
    recipe1["indexTags"] = ["Vegan", "Brokkoli", "Pasta"]
    recipe1["author"] = "NA"
    recipe1["cookingSteps"] = ["Zwiebel, Kartoffel und Knoblauch klein schneiden und in Wasser kochen.", "Brokkoli nach einiger Zeit hinzugeben und garen.",
                               "Abseihen, mit Wasser, Gemünd Hüfsamen mixen und aufkochen.", "Abschmecken und mit Pasta ihrer Wahl essen."]
    recipe1["waitTime"] = "0"
    recipe1["prepTime"] = "30"
    recipe1["ingredients"] = {"": ["250g Brokkoli", "100g Zwiebel", "100g Kartoffel",
                                   "2 Knoblauchzehen", "30g Hanfsamen", "350 ml Wasser", "1 El Hefeflocken", "Gemüebrüünpulver"]}
    recipe1["portionSize"] = "2 Portionen"
    recipe1["pictureFile"] = "pictures\\brokkoli-sauce-vegan.jpg"
    recipe1["category"]="Allgemein"
    recipe1["id"] = 1
    recipes = {}
    recipes[recipe1["recipeTitle"]] = recipe1
    return recipes
