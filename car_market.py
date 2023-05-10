import json

from database import DataBase
from car import Car
import messages


class CarMarket:
    def __init__(self, database, config_json):
        with open(config_json, 'r') as f:
            conf = json.load(f)

        self.db = database
        self.__cars_file = conf['car_list']
        self.__history_file = conf['payment_history']
        self.car_list = self.db.load(self.__cars_file)
        self.__payment_history = self.db.load(self.__history_file)

    def add_car(self, car_ob):
        if car_ob.model not in self.car_list:
            self.car_list[car_ob.model] = {'color': car_ob.color.capitalize(),
                                           'price': car_ob.price,
                                           'discount': car_ob.discount}
            self.db.save(self.car_list, self.__cars_file)
            print(f'{messages.car_added}')
        else:
            print(f'{messages.car_already_exist}')

    def __remove_car(self, car_model):
        if car_model in self.car_list:
            del self.car_list[car_model]
            self.db.save(self.car_list, self.__cars_file)
            print(f'{messages.car_del}')
        else:
            print(f'{messages.car_not_exists}')

    def _set_discount(self, car_model, discount):
        if car_model in self.car_list:
            self.car_list[car_model]['discount'] = discount
            self.db.save(self.car_list, self.__cars_file)
            print(f'{messages.set_discout}')
        else:
            print(f'{messages.car_not_exists}')

    def get_sold_car_history(self):
        return self.__payment_history

    # def return_car(self):

    # def _get_seller_available_cars(self,seller_name, seller_surname):

    def get_car_available_discount(self, car_model):
        if car_model in self.car_list:
            if self.car_list[car_model]['discount']:
                print(f"Discount of {car_model} is: {self.car_list[car_model]['discount']}%..")
            else:
                print(f'{messages.no_discount}')
        else:
            print(f'{messages.car_not_exists}')


if __name__ == '__main__':

    db = DataBase()

    c = CarMarket(db, 'filename_config.json')
    car1 = Car('BMW E34', 'red', 40000)
    # c.get_car_available_discount('BMW F90')
    # c._set_discount('BMW E60',30)
    # c.add_car(car1)
    # print(c.car_list)
