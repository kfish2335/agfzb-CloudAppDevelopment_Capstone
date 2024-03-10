from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarMake(models.Model):
    Name = models.CharField(max_length=20)
    Description = models.CharField(max_length=20)

    def __str__(self):
        template = '{0.Name} {0.Description}'
        return template.format(self)


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    choice = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "WAGON"),
        ("Van", "Van"),
        ("Sports Car", "Sports Car"),
        ("Truck", "Truck"),
    ]

    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    DealerId = models.IntegerField()
    Year = models.DateField()
    Type = models.CharField(
        max_length=10,
        choices=choice,
    )

    def __str__(self):
        template = '{0.Name} {0.DealerId} {0.Year} {0.Type}'
        return template.format(self)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name
    

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, id, purchase_date, car_make, car_model, car_year, review, sentiment):
        
        self.dealership = dealership
        
        self.name = name
        
        self.purchase = purchase
        
        self.id = id
        
        self.purchase_date = purchase_date
        
        self.car_make = car_make
        
        self.car_model = car_model

        self.car_year = car_year
       
        self.sentiment = sentiment

        self.review = review
    def __str__(self):
        return "Dealer Review: " + self.name