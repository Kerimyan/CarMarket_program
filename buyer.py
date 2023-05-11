from person import Person


class Buyer(Person):
    def __init__(self, name, surname, city, money, car_market, data_obct):
        super().__init__(name, surname, city)
        self.db = data_obct
        self.car_market = car_market

        """Creating buyer's bank account if not exist.."""
        self.account_file = f"{self.name}'s_bank_account.json"

        try:
            self.account = self.db.load(self.account_file)
        except FileNotFoundError:
            form_dict = {'money': money, 'spent_money': 0}
            self.db.save(form_dict, self.account_file)
            self.account = self.db.load(self.account_file)



        # self.money = None
        # self.spent_money = None
        # self.bought_cars = None


if __name__ == '__main__':
    b = Buyer('a', 'df', 'c')
    print(b.__dict__)
