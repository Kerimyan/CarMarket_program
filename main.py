from car_market import CarMarket
from database import DataBase
from seller import Seller
from buyer import Buyer
from car import Car
import messages

if __name__ == '__main__':
    database = DataBase()
    config_file = 'filename_config.json'
    market = CarMarket(database, config_file, Seller, Buyer)

    print(messages.usage)
    while True:
        command = input('|=====>').upper()

        if command == 'ADD CAR':
            try:
                model = input(messages.ent_model)
                color = input(messages.ent_color)
                price = int(input(messages.ent_price))
                discount = input(messages.ent_discount)
                if discount == '':
                    discount = None
                else:
                    discount = int(discount)
                car = Car(model, color, price, discount=discount)
            except ValueError:
                print(messages.fail)
                continue
            if car:
                market.add_car(car)

        elif command == 'CREATE ACCOUNT':
            ac_type = input(messages.account_type).upper()
            if ac_type == "SELLER":
                name = input('Enter name-->').capitalize()
                surname = input('Enter surname -->').capitalize()
                city = input('Enter city -->').capitalize()
                n = int(input(messages.n_of_car))
                avlb_cars = []
                for i in range(n):
                    av_car = input('Enter car-->')
                    avlb_cars.append(av_car)
                if name and surname and city and avlb_cars:
                    print(avlb_cars)
                    market.create_seller(name, surname, city, avlb_cars)
                    print(messages.create_account.format(type='Seller'))
                else:
                    print(messages.fail)

            elif ac_type == "BUYER":
                try:
                    name = input('Enter name-->').capitalize()
                    surname = input('Enter surname -->').capitalize()
                    city = input('Enter city -->').capitalize()
                    money = int(input(messages.buyer_money))
                    if name and surname and city and money:
                        market.create_buyer(name, surname, city, money)
                        print(messages.create_account.format(type='Buyer'))
                except ValueError:
                    print(messages.fail)

            else:
                print(messages.fail)

        elif command == 'LOG IN':
            sing_to = input(messages.log_in_to).upper()
            if sing_to == 'SELLER':
                print([seller for seller in market.seller_list.keys()])
                seller_name = input(messages.which_account)

                if seller_name in market.seller_list:
                    seller = market.seller_list[seller_name]
                    print(messages.seller_usage)

                    while True:
                        command = input(f'{seller_name} +===> ').upper()
                        if command == "EXIT":
                            break

                        elif command == "CAR PARK":
                            seller.get_cars_from_carpark()

                        elif command == "BALANCE":
                            print(f'Balance --. {seller.money}$')

                        elif command in ("HELP", "H", "?"):
                            print(messages.seller_usage)

                        else:
                            if command != "":
                                print(messages.fail)

                else:
                    print(messages.fail)

            elif sing_to == 'BUYER':
                print([buyer for buyer in market.buyer_list.keys()])
                buyer_name = input(messages.which_account)
                if buyer_name in market.buyer_list:
                    buyer = market.buyer_list[buyer_name]
                    print(messages.buyer_usage)
                    while True:
                        command = input(f'{buyer_name} +===> ').upper()
                        if command == 'BUY CAR':
                            model = input(messages.ent_model)
                            if model:
                                buyer.buy_car(model)
                            else:
                                print(messages.fail)

                        elif command == 'ALL CARS':
                            buyer.print_my_cars()

                        elif command == 'RETURN CAR':
                            ret_model = input(messages.ent_model)
                            buyer.return_car(ret_model)

                        elif command == 'BALANCE':
                            print(f'Balance --> {buyer.money} $')
                            print(f'Spent Money --> {buyer.spent_money} $')

                        elif command in ('HELP', 'H', '?'):
                            print(messages.buyer_usage)

                        elif command == 'EXIT':
                            break

                        else:
                            if command != '':
                                print(messages.fail)

                else:
                    print(messages.fail)
            else:
                print(messages.fail)

        elif command in ('HELP', 'H', '?'):
            print(messages.usage)

        elif command == 'EXIT':
            break

        else:
            if command != '':
                print(messages.fail)
