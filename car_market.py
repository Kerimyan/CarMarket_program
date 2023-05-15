import messages
from uuid import uuid4


class CarMarket:
    def __init__(self, database, config_json, seller_class, buyer_class):
        self.db = database
        self.SellerClass = seller_class
        self.BuyerClass = buyer_class
        conf = self.db.load(config_json)
        self.__cars_file = conf['car_list']
        self.__history_file = conf['payment_history']
        self.__account_info_file = conf['account_info_file']
        self.car_list = self.db.load(self.__cars_file)
        self.__payment_history = self.db.load(self.__history_file)

        self.account_info = self.db.load(self.__account_info_file)

        """Creating seller accounts"""
        self.seller_list = {}
        seller_info = self.account_info['seller_info']
        if seller_info:
            for info in seller_info:
                self.create_seller(**info)

        """Creating buyer accounts"""
        self.buyer_list = {}
        buyer_info = self.account_info['buyer_info']
        if buyer_info:
            for info in buyer_info:
                self.create_buyer(**info)

    def create_seller(self, name, surname, city, available_cars_list):
        seller = self.SellerClass(name, surname, city, self.db, self, available_cars_list)
        name_surname = name + ' ' + surname
        self.seller_list[name_surname] = seller
        info = {'name': name,
                'surname': surname,
                'city': city,
                'available_cars_list': available_cars_list}
        if info not in self.account_info['seller_info']:
            self.account_info['seller_info'].append(info)
            self.db.save(self.account_info, self.__account_info_file)

    def create_buyer(self, name, surname, city, money):
        buyer = self.BuyerClass(name, surname, city, money, self, self.db)
        name_surname = name + ' ' + surname
        self.buyer_list[name_surname] = buyer
        info = {'name': name,
                'surname': surname,
                'city': city,
                'money': money}
        if info not in self.account_info['buyer_info']:
            self.account_info['buyer_info'].append(info)
            self.db.save(self.account_info, self.__account_info_file)

    def add_car(self, car_ob):
        car_id = str(uuid4())
        self.car_list[car_id] = {'model': car_ob.model,
                                 'color': car_ob.color.capitalize(),
                                 'price': car_ob.price,
                                 'discount': car_ob.discount,
                                 'seller': None}
        self.db.save(self.car_list, self.__cars_file)
        print(messages.car_added)

    def sell_car(self, car_model, buyer):
        seller = self.__search_seller(car_model)
        if seller:
            car = seller.sell_car(car_model, buyer)
            self.set_payment_history(car)
            return car
        else:
            return None

    def __search_seller(self, car_model):
        for seller in self.seller_list.values():
            for car in seller.available_cars_list:
                if car == car_model:
                    return seller
        else:
            return None

    def __remove_car(self, car_id):
        if car_id in self.car_list:
            del self.car_list[car_id]
            self.db.save(self.car_list, self.__cars_file)
        else:
            print(messages.car_not_exists)

    def _set_discount(self, car_model, discount):
        if isinstance(discount, (int, float)):
            for car_m in self.car_list.values():
                if car_model == car_m['model']:
                    car_m['discount'] = discount
            self.db.save(self.car_list, self.__cars_file)
        else:
            raise ValueError

    def set_payment_history(self, car):
        car_id = list(car.keys())[0]
        self.__payment_history.append(car)
        self.__remove_car(car_id)
        self.db.save(self.__payment_history, self.__history_file)

    def get_sold_car_history(self):
        for hist in self.__payment_history:
            c_id = list(hist.keys())[0]
            print(f"||ID -- {c_id}")
            print(f"||{hist[c_id]}")
            print(50 * '____')

    def _get_seller_available_cars(self, seller, available_car_list):
        res_dict = {}
        for c_id, car in self.car_list.items():
            if car['model'] in available_car_list:
                self.car_list[c_id]['seller'] = {'name': seller.name,
                                                 'surname': seller.surname,
                                                 'city': seller.city}
                res_dict[c_id] = self.car_list[c_id]
        self.db.save(self.car_list, self.__cars_file)
        return res_dict

    def get_car_available_discount(self, car_model):
        for car_m in self.car_list.values():
            if car_model == car_m['model'] and car_m['discount']:
                print(f"Discount of {car_m['model']} is {car_m['discount']}%")
                break
        else:
            print(messages.no_discount)

    def return_car(self, car, buyer):
        car_id = list(car.keys())[0]
        seller = self.__search_seller(car[car_id]['model'])
        buyer_form = {'buyer': {'name': buyer.name,
                                'surname': buyer.surname,
                                'city': buyer.city}}
        car[car_id].update(buyer_form)
        car[car_id]['status'] = 'Returned'
        self.__payment_history.append(car)
        self.db.save(self.__payment_history, self.__history_file)
        del car[car_id]['status']
        del car[car_id]['buyer']
        self.car_list.update(car)
        self.db.save(self.car_list, self.__cars_file)
        seller.return_car(car)
