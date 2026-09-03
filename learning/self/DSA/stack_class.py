# 1. The Blueprint
class Stack:
    
    # 2. Attributes (The Data)
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.arr = [0] * capacity   # Array sized to the chosen capacity
        self.top = -1               # Index of the current top element

    # 3. Helper status methods
    def is_full(self):
        """Returns True if the stack has reached maximum capacity."""
        return self.top == self.capacity - 1

    def is_empty(self):
        """Returns True if the stack has no elements."""
        return self.top == -1

    # 4. Core Actions (Methods)
    def push(self, x):
        """Adds an element to the top of the stack if not full."""
        if self.is_full():
            print(f"Stack Overflow! Cannot add {x}, stack is full (capacity: {self.capacity}).")
            return False
        
        self.top += 1
        self.arr[self.top] = x
        print(f"Added {x} to the stack! (Current elements: {self.arr[:self.top + 1]})")
        return True

    def pop(self):
        """Removes and returns the top element from the stack if not empty."""
        if self.is_empty():
            print("Stack Underflow! Cannot pop from an empty stack.")
            return None
        
        popped_value = self.arr[self.top]
        self.arr[self.top] = 0      # Optional: reset slot back to 0
        self.top -= 1
        print(f"Popped {popped_value} from the stack!")
        return popped_value

    def peek(self):
        """Returns the top element without removing it."""
        if self.is_empty():
            print("Stack is empty, nothing to peek at.")
            return None
        return self.arr[self.top]

    def size(self):
        """Returns the current number of elements in the stack."""
        return self.top + 1


# ==========================================
# 5. Using the Blueprint outside the class
# ==========================================

# Example 1: Using default capacity (5)
print("--- Stack with default capacity (5) ---")
my_stack = Stack()
my_stack.push(10)
my_stack.push(20)

# Example 2: Creating a custom capacity stack (capacity = 3)
print("\n--- Stack with custom capacity (3) ---")
small_stack = Stack(capacity=3)
small_stack.push(1)
small_stack.push(2)
small_stack.push(3)
small_stack.push(4)  # This will trigger the capacity limit!

# Example 3: Pop and Peek
print("\nTop element:", small_stack.peek())
small_stack.pop()
print("After pop, top element:", small_stack.peek())