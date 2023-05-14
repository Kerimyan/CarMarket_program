from person import Person
from car_market import CarMarket
from database import DataBase
from seller import Seller
import messages


class Buyer(Person):
    def __init__(self, name, surname, city, money, car_market, data_obct):
        super().__init__(name, surname, city)
        self.db = data_obct
        self.car_market = car_market

        """Creating buyer's bank account if not exist.."""
        self.account_file = f"{self.name}'s_bank_account.json"

        try:
            self.bank_account = self.db.load(self.account_file)
        except FileNotFoundError:
            form_dict = {'money': money, 'spent_money': 0}
            self.db.save(form_dict, self.account_file)
            self.bank_account = self.db.load(self.account_file)
        self.money = self.bank_account['money']
        self.spent_money = self.bank_account['spent_money']

        """Creating buyer's garage if not exist..."""
        self.bought_cars_file = f"{self.name}'s_garage.json"

        try:
            self.bought_cars = self.db.load(self.bought_cars_file)
        except FileNotFoundError:
            self.db.save({}, self.bought_cars_file)
            self.bought_cars = self.db.load(self.bought_cars_file)

    def buy_car(self, car_model):
        bought_car = self.car_market.sell_car(car_model, self)
        if bought_car:
            car_id = list(bought_car.keys())[0]
            price = bought_car[car_id]['price']
            self.__change_money(price, '-')
            del bought_car[car_id]['buyer']
            self.add_bought_car(bought_car)
        else:
            print(messages.car_not_sale)

    def __change_money(self, price, up_dow):
        if up_dow == '+':
            self.money += price
            self.spent_money -= price
        else:
            self.money -= price
            self.spent_money += price
        self.bank_account['money'] = self.money
        self.bank_account['spent_money'] = self.spent_money
        self.db.save(self.bank_account, self.account_file)

    def add_bought_car(self, car):
        self.bought_cars.update(car)
        self.db.save(self.bought_cars, self.bought_cars_file)

    def print_my_cars(self):
        for car in self.bought_cars.values():
            print(f'{car["model"]}  --{car["color"]}--')

    def return_car(self, car_model):
        for c_id, car in self.bought_cars.items():
            if car_model == car['model']:
                ret_car = {c_id: car}
                price = self.bought_cars[c_id]['price']
                del self.bought_cars[c_id]
                self.db.save(self.bought_cars, self.bought_cars_file)
                break
        self.__change_money(price, '+')
        self.car_market.return_car(ret_car, self)
