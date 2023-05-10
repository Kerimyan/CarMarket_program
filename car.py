class Car:
    def __init__(self, model, color, price, discount=None):
        if type(model) is str and type(color) is str and type(price) is int:
            self._model = model
            self._color = color
            self._price = price
        else:
            raise ValueError
        self._discount = discount

    @property
    def model(self):
        return self._model

    @property
    def color(self):
        return self._color

    @property
    def price(self):
        return self._price

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if isinstance(value, int):
            self._discount = value
        else:
            raise ValueError
