from datetime import date
from get_requests import *

class DiningInfo:
    def __init__(self):
        self.table = dict()
        self.dining_h = ["east-quad", "bursley", "markley", "mosher-jordan", "north-quad", "south-quad", "twigs-at-oxford"]

    def find_all_foods_dining(self, dining_hall_nm):
        ret = []
        raw_html = simple_get("https://dining.umich.edu/menus-locations/dining-halls/" + dining_hall_nm)
        b = BeautifulSoup(raw_html, 'html.parser')
        rs = b.find_all("div", class_ = "item-name")
        
        for item in rs:
            ret.append(item.text)
        return ret

    # finds a substr regardless of case
    def find_string_in_list(self, lis, target):
        return any(target in l.lower() for l in lis)

    def find_salmon(self):
        for d in self.dining_h:
            all_food = self.find_all_foods_dining(d)
            print(all_food)
            if self.find_string_in_list(all_food, "salmon"):
                self.table[d] = True

    def get_table(self):
        return self.table


if __name__ == "__main__":
    d = DiningInfo()
    d.find_salmon()
    print(d.get_table())
    today = date.today()


