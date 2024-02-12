class Transport:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def display_info(self):
        return f"The {self.brand} was released in {self.year} "


class Car(Transport):
    def __init__(self, brand, year, color, model, price):
        super().__init__(brand, year)
        self.color = color
        self.model = model
        self.price = price

    def info(self):
        return f"The car with the brand name: {self.brand} model: {self.model} color: {self.color} price: {self.price} was released in {self.year} year"


class Motorcycle(Transport):
    def __init__(self, brand, year, model, speed, color):
        super().__init__(brand, year)
        self.model = model
        self.speed = speed
        self.color = color

    def moto_info(self):
        return f"The motorcycle with the brand name: {self.brand} model: {self.model} color: {self.color} speed: {self.speed} was released in {self.year} year"


car = Car("Chevrolet", 2020, "white", "Html", 3000000)
d = car.info()
print(d)

moto = Motorcycle("Ferrari", 2012, "Xl", 1000, "blue")
res = moto.moto_info()
print(res)
