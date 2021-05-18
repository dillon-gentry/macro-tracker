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

url_code_file = open("working_url_codes.txt", "r+")
url_codes = url_code_file.readlines()
food_codes = []
for code in url_codes:
    new_code = code.strip('\n')
    food_codes.append(new_code)

print(food_codes)

# food_codes = []   #use this chunk to test random url codes to expand data in a fast and smart manner
# for i in range(0, 10000):
#     n = random.randint(000000, 999999)
#     n_str = str(n)
#     n_len = len(n_str)
#     new_str = ''
#     if n_len < 6:
#         while n_len < 6:
#             n_str = '0' + n_str
#             n_len += 1
#     food_codes.append(n_str)
# print(food_codes)

food_data = []

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

# url= "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort=000000*1"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")
# print(soup) #for html
# print(soup.get_text()) #for text inside html tags


for i in food_codes:
    url = "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort="+i+"*1"
    # if i == 0:
    #     url = "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort=201014*1" #cantaloupe
    # if i == 1:
    #     url = "http://hf-food.austin.utexas.edu/foodpro/label.aspx?locationNum=12&locationName=Jester+2nd+Floor+(J2)+Dining&dtdate=5%2f16%2f2021&RecNumAndPort=117004*1" #grilled chicken sandwich
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    recipe_check = soup.find("div", class_="labelnotavailable")
    skip = False

    # if recipe_check != None: used for checking codes for the first time
    #     dne_file = open("dne_url_codes.txt", "a")
    #     dne_file.write(i+'\n')
    #     print('recipe not found for code ' + i)
    #     skip = True
    # else:
    #     recipe_name_check = soup.find("div", class_="labelrecipe").text
    #     if recipe_name_check == '':
    #         empty_file = open("empty_url_codes.txt", "a")
    #         empty_file.write(i+'\n')
    #         print('recipe empty for code ' + i)
    #         skip = True
    #     else:
    #         exists_file = open("working_url_codes.txt", "a")
    #         exists_file.write(i+'\n')
    #         print('recipe exists for code ' + i)

    if skip == False:

        recipe_name = soup.find("div", class_="labelrecipe").text
        # print(recipe_name)

        serv_size = soup.find_all("div", class_="nutfactsservsize")[1].text
        # print(serv_size)

        cals = soup.find("td", class_="nutfactscaloriesval").text
        # print(cals)

        nutrients = soup.find_all("span", class_="nutfactstopnutrient")
        for j in range(0, len(nutrients)):
            # print(nutrients[i].text)

            s = nutrients[j].text

            # Total Fat #g
            if s.startswith("Total Fat"):
                # print(s)
                tot_fat = s.rsplit("\xa0")[1]
                # print(tot_fat)

            # Saturated Fat #g
            if s.startswith("Saturated Fat"):
                # print(s)
                sat_fat = s.rsplit("\xa0")[1]
                # print(sat_fat)

            # Trans Fat #g
            if s.startswith("Trans Fatty Acid"):
                # print(s)
                trans_fat = s.rsplit("\xa0")[1]
                # print(trans_fat)

            # Carbohydrates #g
            if s.startswith("Carbohydrates"):
                # print(s)
                carbs = s.rsplit("\xa0")[1]
                # print(carbs)

            # Total Sugars #g
            if s.startswith("Total Sugars"):
                # print(s)
                tot_sug = s.rsplit("\xa0")[1]
                # print(tot_sug)

            # Added Sugar #g
            if s.startswith("Added Sugar"):
                # print(s)
                added_sug = s.rsplit("\xa0")[1]
                # print(added_sug)

            # Protein #g
            if s.startswith("Protein"):
                # print(s)
                protein = s.rsplit("\xa0")[1]
                # print(protein)

            # Dietary Fiber #g
            if s.startswith("Dietary Fiber (2016)"):
                # print(s)
                diet_fib = s.rsplit("\xa0")[1]
                # print(diet_fib)

            # Sodium #mg
            if s.startswith("Sodium"):
                # print(s)
                sodium = s.rsplit("\xa0")[1]
                # print(sodium)

            # Cholesterol #mg
            if s.startswith("Cholesterol"):
                # print(s)
                cholest = s.rsplit("\xa0")[1]
                # print(cholest)

            # Total Carbohydrate. #g

            # Vitamin D - mcg #mcg

            # Calcium #mg

            # Iron #mg

            # Potassium #mg

        food_data_obj = FoodDataObj(recipe_name, serv_size, cals, tot_fat, sat_fat, trans_fat, carbs, tot_sug,
                                    added_sug, protein, diet_fib, sodium, cholest)

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

        food_data.append(food_data_obj)

print(food_data)

# food_data object created, now use CRUD operations to add to database
