
class Product:
    def __init__(self, name, description = False, catalogue_number=False, brand=False, pack_size=False, price=False, availability=False):
        self.name = name
        self.description = description
        self.catalogue_number = catalogue_number
        self.pack_size = pack_size
        self.brand = brand
        self.price = price
        self.availability = availability
        
        if self.description == False:
            self.description = ""
    
    def __str__(self):
        return """{self.name}, {self.description}{self.catalogue_number}, {self.availability} **{self.pack_size}**, **{self.price}** """.format(self=self)

