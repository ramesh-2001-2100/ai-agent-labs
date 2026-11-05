try:
    x = int(input("Enter a number: "))
    print(f"The number is {x}")
except ValueError:
    print("Invalid input. Please enter a valid number.")
