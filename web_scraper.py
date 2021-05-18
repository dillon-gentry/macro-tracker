from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random


class FoodDataObj:

    def __init__(self, recipe_name, serv_size, cals, tot_fat, sat_fat, trans_fat, carbs, tot_sug,
                 added_sug, protein, diet_fib, sodium, cholest):
        self.recipe_name = recipe_name
        self.serv_size = serv_size
        self.cals = cals
        self.tot_fat = tot_fat
        self.sat_fat = sat_fat
        self.trans_fat = trans_fat
        self.carbs = carbs
        self.tot_sug = tot_sug
        self.added_sug = added_sug
        self.protein = protein
        self.diet_fib = diet_fib
        self.sodium = sodium
        self.cholest = cholest


food_codes_ex = ['201014', '117004', '111111', '000000']


def findNewURLCodes(num):
    new_codes = []  # use this chunk to test random url codes to expand data in a fast and smart manner
    for i in range(0, num):
        n = random.randint(000000, 999999)
        n_str = str(n)
        n_len = len(n_str)
        new_str = ''
        if n_len < 6:
            while n_len < 6:
                n_str = '0' + n_str
                n_len += 1
        new_codes.append(n_str)
    return new_codes


def getURLCodes():
    url_code_file = open("working_url_codes.txt", "r+")
    url_codes = url_code_file.readlines()
    food_codes = []
    for code in url_codes:
        new_code = code.strip('\n')
        food_codes.append(new_code)
    url_code_file.close()
    return food_codes


def recordURLCodes(new_codes):
    for i in new_codes:
        url = "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort="+i+"*1"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        recipe_check = soup.find("div", class_="labelrecipe")

        if recipe_check != None:  # used for checking codes for the first time
            dne_file = open("dne_url_codes.txt", "a")
            dne_file.write(i+'\n')
            print('recipe not found for code ' + i)
            skip = True
        else:
            recipe_name_check = soup.find("div", class_="labelrecipe").text
            if recipe_name_check == '':
                empty_file = open("empty_url_codes.txt", "a")
                empty_file.write(i+'\n')
                print('recipe empty for code ' + i)
                skip = True
            else:
                exists_file = open("working_url_codes.txt", "a")
                exists_file.write(i+'\n')
                print('recipe exists for code ' + i)


def getFoodData(food_codes):

    food_data = []
    for i in food_codes:
        recipe_name = ''
        serv_size = ''
        cals = ''
        tot_fat = ''
        sat_fat = ''
        trans_fat = ''
        carbs = ''
        tot_sug = ''
        added_sug = ''
        protein = ''
        diet_fib = ''
        sodium = ''
        cholest = ''

        url = "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort="+i+"*1"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        recipe_name = soup.find("div", class_="labelrecipe").text
        # print(recipe_name)

        serv_size = soup.find_all("div", class_="nutfactsservsize")[1].text
        # print(serv_size)

        cals = soup.find("td", class_="nutfactscaloriesval").text
        # print(cals)

        nutrients = soup.find_all("span", class_="nutfactstopnutrient")
        for j in range(0, len(nutrients)):

            s = nutrients[j].text

            # Total Fat #g
            if s.startswith("Total Fat"):
                tot_fat = s.rsplit("\xa0")[1]

            # Saturated Fat #g
            if s.startswith("Saturated Fat"):
                sat_fat = s.rsplit("\xa0")[1]

            # Trans Fat #g
            if s.startswith("Trans Fatty Acid"):
                trans_fat = s.rsplit("\xa0")[1]

            # Carbohydrates #g
            if s.startswith("Carbohydrates"):
                carbs = s.rsplit("\xa0")[1]

            # Total Sugars #g
            if s.startswith("Total Sugars"):
                tot_sug = s.rsplit("\xa0")[1]

            # Added Sugar #g
            if s.startswith("Added Sugar"):
                added_sug = s.rsplit("\xa0")[1]

            # Protein #g
            if s.startswith("Protein"):
                protein = s.rsplit("\xa0")[1]

            # Dietary Fiber #g
            if s.startswith("Dietary Fiber (2016)"):
                diet_fib = s.rsplit("\xa0")[1]

            # Sodium #mg
            if s.startswith("Sodium"):
                sodium = s.rsplit("\xa0")[1]

            # Cholesterol #mg
            if s.startswith("Cholesterol"):
                cholest = s.rsplit("\xa0")[1]

        food_data_obj = FoodDataObj(recipe_name, serv_size, cals, tot_fat, sat_fat, trans_fat, carbs, tot_sug,
                                    added_sug, protein, diet_fib, sodium, cholest)
        food_data.append(food_data_obj)
    return food_data


def printFoodDataObj(food_data_obj):
    print(food_data_obj.recipe_name)
    print(food_data_obj.serv_size)
    print(food_data_obj.cals)
    print(food_data_obj.tot_fat)
    print(food_data_obj.sat_fat)
    print(food_data_obj.trans_fat)
    print(food_data_obj.carbs)
    print(food_data_obj.tot_sug)
    print(food_data_obj.added_sug)
    print(food_data_obj.protein)
    print(food_data_obj.diet_fib)
    print(food_data_obj.sodium)
    print(food_data_obj.cholest)


food_codes = getURLCodes()
# print(food_codes)
print(len(food_codes))
food_data = getFoodData(food_codes)
# print(food_data)
print(len(food_data))
# for food in food_data:
#     printFoodDataObj(food)
