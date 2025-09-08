class Robot:
    category = "AI Humanoid"
    capability = "Multilingual"

# Access via class
print(Robot.category)     # AI Humanoid
print(Robot.capability)   # Multilingual

# Access via objects (also works)
r1 = Robot()
print(r1.category)        # AI Humanoid
