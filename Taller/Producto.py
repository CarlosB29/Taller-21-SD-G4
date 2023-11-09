import pickle

class Producto:
    def __init__(self, name, category, precio):
        self.name = name
        self.category = category
        self.precio = precio

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_precio(self):
        return self.precio
