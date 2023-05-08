class Car:
    def __init__(self, mark, model, color, price):
        self._mark = mark
        self._model = model
        self._color = color
        self._price = price

    @property
    def mark(self):
        return self._mark
    
    @property
    def model(self):
        return self._model

    @property
    def color(self):
        return self._color

    @property
    def price(self):
        return self._price

