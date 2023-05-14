import messages
import datetime
from person import Person
from database import DataBase


class Seller(Person):
    def __init__(self, name, surname, city, data_obct, car_market, available_cars_list):
        super().__init__(name, surname, city)
        self.db = data_obct
        self.car_market = car_market
        self.available_cars_list = available_cars_list

        """Creating an account if not exist.."""
        self.account_file = f"{self.name}'s_account.json"

        try:
            self.account = self.db.load(self.account_file)
        except FileNotFoundError:
            form_dict = {'money': 0, 'sold_cars': {}}
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
        return self.car_market._get_seller_available_cars(self, av_car_list)

    def sell_car(self, car_model, buyer):
        car_for_sell = {}
        day_time = str(datetime.date.today())
        for id, car in self.car_park.items():
            if car_model == car['model']:
                price = self._check_discount(id)
                car_for_sell[id] = car
                car_for_sell[id]['price'] = price
                del car_for_sell[id]['discount']
                car_for_sell[id]['data'] = day_time
                self.__change_money(price, '+')
                car_for_sell[id]['buyer'] = {'name': buyer.name, 'surname': buyer.surname, 'city': buyer.city}
                self.add_sold_car(car_for_sell, id)
                car_for_sell[id]['seller'] = {'name': self.name, 'surname': self.surname, 'city': self.city}
                del self.car_park[id]
                self.db.save(self.car_park, self.car_park_file)
                print(messages.car_sold.format(car=car_model))
                return car_for_sell
        else:
            print(messages.seller_car_not_exists.format(name=self.name, surname=self.surname))

    def _check_discount(self, car_id):
        if self.car_park[car_id]['discount']:
            return self.car_park[car_id]['price'] * self.car_park[car_id]['discount'] // 100
        else:
            return self.car_park[car_id]['price']

    def __change_money(self, price, up_dow):
        if up_dow == '+':
            self.money += price
        else:
            self.money -= price
        self.account['money'] = self.money
        self.db.save(self.account, self.account_file)

    def add_sold_car(self, car, id):
        self.account['sold_cars'].update(car)
        del self.account['sold_cars'][id]['seller']
        self.db.save(self.account, self.account_file)

    def return_car(self, car):
        car_id = list(car.keys())[0]
        price = car[car_id]['price']
        self.__change_money(price, '-')
        del self.sold_cars[car_id]
        self.account['sold_car'] = self.sold_cars
        self.db.save(self.account, self.account_file)
        self.car_park.update(car)
        self.db.save(self.car_park, self.car_park_file)
