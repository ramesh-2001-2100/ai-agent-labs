class Dog:
    total_dogs = 0  # Class variable (shared by ALL dogs)
    
    def __init__(self, name):
        self.name = name
        Dog.total_dogs += 1  # Increase the count
    
    @classmethod
    def how_many_dogs(cls):  # cls goes here!
        return f"There are {cls.total_dogs} dogs"

dog1 = Dog("Buddy")
dog2 = Dog("Max")
dog3 = Dog("Charlie")

print(Dog.how_many_dogs())  # There are 3 dogs
