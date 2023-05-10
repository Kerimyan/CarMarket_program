from person import Person


class Buyer(Person):
    def __init__(self, name, surname, city):
        super().__init__(name, surname, city)
        self.money = None
        self.spent_money = None
        self.bought_cars = None


if __name__ == '__main__':
    b = Buyer('a', 'df', 'c')
    print(b.__dict__)
