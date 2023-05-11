import messages
import datetime
from person import Person
from database import DataBase
from car_market import CarMarket

from buyer import Buyer


class Seller(Person):
    def __init__(self, name, surname, city, data_obct, car_market, available_cars_list):
        super().__init__(name, surname, city)
        self.db = data_obct
        self.car_market = car_market

        """Creating an account if not exist.."""
        self.account_file = f"{self.name}'s_account.json"

        try:
            self.account = self.db.load(self.account_file)
        except FileNotFoundError:
            form_dict = {'money': 0, 'sold_cars': None}
            self.db.save(form_dict, self.account_file)
            self.account = self.db.load(self.account_file)
        self.money = self.account['money']
        self.sold_cars = self.account['sold_cars']

        """Creating car_park if not exist..."""
        self.car_park_file = f"{self.name}'s_car_park.json"

        try:
            self.car_park = self.db.load(self.car_park_file)
        except FileNotFoundError:
            av_cars = self._get_available_cars(available_cars_list)
            self.db.save(av_cars, self.car_park_file)
            self.car_park = self.db.load(self.car_park_file)

    def _get_available_cars(self, av_car_list):
        return self.car_market._get_seller_available_cars(av_car_list)

    def sell_car(self, car_model, buyer):
        if car_model in self.car_park:
            car = {'model': car_model, 'color': self.car_park[car_model]['color'], 'seller': self}
            price = self._check_discount(car_model)
            self.__change_money(price, '+')
            self.add_sold_car(car, buyer)
            del self.car_park[car_model]
            self.db.save(self.car_park, self.car_park_file)
            print(messages.car_sold.format(car=car_model))
            return car, price
        else:
            print(messages.seller_car_not_exists.format(name=self.name, surname=self.surname))

    def _check_discount(self, car_model):
        if self.car_park[car_model]['discount']:
            return self.car_park[car_model]['price'] * self.car_park[car_model]['discount'] // 100
        else:
            return self.car_park[car_model]['price']

    def __change_money(self, price, up_dow):
        if up_dow == '+':
            self.money += price
        else:
            self.money += price
        self.account['money'] = self.money
        self.db.save(self.account, self.account_file)

    def add_sold_car(self, car, buyer):
        car['buyer'] = {'name': buyer.name, 'surname': buyer.surname, 'city': buyer.city}
        del car['seller']
        car['data'] = str(datetime.date.today())
        self.account['sold_cars'] = car
        db.save(self.account, self.account_file)


if __name__ == '__main__':
    db = DataBase()
    c = CarMarket(db, 'filename_config.json')
    cars = ['BMW E60', 'Ford Fusion', 'Merc']
    s = Seller('John', 'Wick', 'New-York', db, c, cars)
    car = {'model': 'z4', 'color': 'red', 'seller': s}
    b = Buyer('Mik', 'Dev', 'NEW')
    s.sell_car('BMW E60', b)
    # print(s.add_sold_car(car, b))
