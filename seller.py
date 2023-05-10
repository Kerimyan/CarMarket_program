from person import Person


class Seller(Person):
    def __init__(self, name, surname, city):
        super().__init__(name, surname, city)
        self.money = None
        self.car_park = None
        self.sold_cars = None


if __name__ == '__main__':
    s = Seller('sa', 'zx', 'g')
