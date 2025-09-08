# Problem Statement: Create a class Robo with a 
# class attribute category = "AI Humanoid". 
# Add an __init__() method to assign name, model, and year as instance attributes. Create two objects: chitti and sparky.

# 🎯 Expected Output:

# Chitti (Model V2.0, Year 2025) - Category: AI Humanoid  
# Sparky (Model X1, Year 2023) - Category: AI Humanoid


class Robo:
    category = "AI Humanoid"


    # static method
    @staticmethod
    def welcome_message():
        print("Welcome to Robo World! All systems are AI-powered.")

     # class method
    @classmethod
    def show_category(cls):
        print(f"All robos belong to category: {cls.category}")
    
    @classmethod
    def change_category(cls):
        cls.category = "AI Pure robotics"

    #constructor
    def __init__(self, name, model, year ):
        self.name = name
        self.model = model 
        self.year = year 

    
    def sing(self):
        print(f"{self.name} is singing melodious song.")

    def dance(self):
        print(f"{self.name} is dancing gracefully on stage...")

    def cook(self):
        print(f"{self.name} is cooking delicious biryani!")

    
    #string representation 
    def __str__(self):
        return f"{self.name} (Model {self.model}, Year {self.year}) - Category: {Robo.category}"


# Creating objects
chitti = Robo("Chitti", "V2.0", 2025)
sparky = Robo("Sparky", "X1", 2023)

# Printing objects
print(chitti)
print(sparky)
chitti.sing()
sparky.cook()

Robo.welcome_message()

print("\nBefore category change:")
print(chitti)
print(sparky)

Robo.change_category()  # change class attribute

print("\nAfter category change:")
print(chitti)
print(sparky)
    
