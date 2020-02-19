from datetime import date
from collections import defaultdict
from get_requests import *
from flask import Flask

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
app = Flask(__name__)
@app.route('/')

def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

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

    def get_html_bursley(self):
        d = DiningInfo(interesting_foods)
        raw_html = simple_get("https://dining.umich.edu/menus-locations/dining-halls/bursley")
        print(BeautifulSoup(raw_html, 'html.parser').prettify())

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
                
    def get_table(self):
        ret = []
        for dh in self.table:
            for food in self.table[dh]:
                foodnm, typef, dhname = food.food_item, food.type_food, food.dining_hall
                printstr = dhname + " has " + foodnm + " in category " + typef + "."
                ret.append(printstr)

        return ret
            

class Email:
    def __init__(self, gmail):
        self.gmail = gmail

    def convert_content_to_html(self, content):
        html = []
        html.append("<html><body><p>")
        for line in content: 
            html.append(str(line))
            html.append("<br>")
        
        html.append("</p></body></html>")
        html = "".join(html)
        return html

    def send_email(self, html, recipient):
        today = str(date)
        me = self.gmail
        my_password = str(open("password.txt").read())
        you = recipient


        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Food at dining halls on " + today
        msg['From'] = me
        msg['To'] = you

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # uncomment if interested in the actual smtp conversation
        # s.set_debuglevel(1)
        # do the smtp auth; sends ehlo if it hasn't been sent already
        s.login(me, my_password)
        s.sendmail(me, you, msg.as_string())
        s.quit()

    def send_emails(self, content, emails):
        c = self.convert_content_to_html(content)
        for email in emails:
            self.send_email(c, email)

        

if __name__ == "__main__":
    
    interesting_foods = ["salmon", "korean", "bbq", "steak"]
    d = DiningInfo(interesting_foods)
    d.find_all_interesting_dishes()
    ret = d.get_table()
    e = Email("nathanzhu12@gmail.com")
    e.send_emails(ret, ["nathanzhu12@gmail.com", "znathan@umich.edu", "hsatam@umich.edu", "chenreny@umich.edu"])


    # d2 = DiningInfo(bad_foods)
    # d2.find_all_interesting_dishes()
    # d2.print_table()



    





    
    # app.run()
    # print(d.get_table())
    # today = date.today()

    