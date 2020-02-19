from datetime import date
from collections import defaultdict
from get_requests import *

class Food:
    # Ex. "Cedar planked salmon", "salmon"
    def __init__(self, food_item_in, type_in, dh):
        self.food_item = food_item_in
        self.type_food = type_in
        self.dining_hall = dh


class DiningInfo:
    # interesting_foods_in is a list of strings repr foods we care about
    def __init__(self, interesting_foods_in):
        self.table = defaultdict(list)
        self.dining_h = ["east-quad", "bursley", "markley", "mosher-jordan", "north-quad", "south-quad", "twigs-at-oxford"]
        self.interesting_foods = interesting_foods_in

    # Literally returns every menu item in a particular dining hall
    def find_all_foods_for_this_dining(self, dining_hall_nm):
        ret = []
        raw_html = simple_get("https://dining.umich.edu/menus-locations/dining-halls/" + dining_hall_nm)
        b = BeautifulSoup(raw_html, 'html.parser')
        rs = b.find_all("div", class_ = "item-name")
        
        for item in rs:
            ret.append(item.text)
        return ret

    # finds a substr regardless of case
    def find_string_in_list(self, lis, dining_hall_in, target_foods):
        for l in lis:
            for food in target_foods:
                if food.lower() in l.lower():
                    self.table[dining_hall_in].append(Food(l, food, dining_hall_in))

    def find_all_interesting_dishes(self):
        for dh in self.dining_h:
            all_food = self.find_all_foods_for_this_dining(dh)
            self.find_string_in_list(all_food, dh, self.interesting_foods)
                
    def print_table(self):
        for dh in self.table:
            for food in self.table[dh]:
                foodnm, typef, dhname = food.food_item, food.type_food, food.dining_hall
                printstr = dhname + " has " + foodnm + " in category " + typef + "."
                print(printstr)
            


if __name__ == "__main__":
    interesting_foods = ["salmon", "korean", "bbq", "steak"]
    bad_foods = ["white fish", "catfish"]
    d = DiningInfo(interesting_foods)
    # raw_html = simple_get("https://dining.umich.edu/menus-locations/dining-halls/bursley")
    # print(BeautifulSoup(raw_html, 'html.parser').prettify())
    d.find_all_interesting_dishes()
    d.print_table()

    d2 = DiningInfo(bad_foods)
    d2.find_all_interesting_dishes()
    d2.print_table()
    # print(d.get_table())
    # today = date.today()