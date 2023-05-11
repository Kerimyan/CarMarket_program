from database import DataBase
from car import Car
import messages


class CarMarket:
    def __init__(self, database, config_json):
        self.db = database
        conf = self.db.load(config_json)
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
            print(messages.car_added)
        else:
            print(messages.car_already_exist)

    def __remove_car(self, car_model):
        if car_model in self.car_list:
            del self.car_list[car_model]
            self.db.save(self.car_list, self.__cars_file)
            print(messages.car_del)
        else:
            print(messages.car_not_exists)

    def _set_discount(self, car_model, discount):
        if car_model in self.car_list and isinstance(discount, int):
            self.car_list[car_model]['discount'] = discount
            self.db.save(self.car_list, self.__cars_file)
            print(messages.set_discout)
        else:
            print(messages.car_not_exists)

    def get_sold_car_history(self):
        return self.__payment_history

    # def return_car(self):

    def _get_seller_available_cars(self,available_car_list):
        res_dict = {}
        for car in available_car_list:
            if car in self.car_list:
                res_dict[car] = self.car_list[car]
                self.__remove_car(car)

        return res_dict


    def get_car_available_discount(self, car_model):
        if car_model in self.car_list:
            if self.car_list[car_model]['discount']:
                print(f"Discount of {car_model} is: {self.car_list[car_model]['discount']}%..")
            else:
                print(messages.no_discount)
        else:
            print(messages.car_not_exists)


if __name__ == '__main__':
    db = DataBase()

    c = CarMarket(db, 'filename_config.json')
    # car1 = Car('E220', 'black', 5000)
    # c.get_car_available_discount('BMW F90')
    # c._set_discount('BMW E60',25)
    # c.add_car(car1)
    # print(c.car_list)
