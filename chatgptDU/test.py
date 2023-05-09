import os
import openai
import foodorder

# User inputs for getting a skill
input_A1 = """Hey there, can I get a coke please?"""
input_A2 = """What kind of shampoo do you guys carry?"""
input_A3 = """I wanna check out my reservation."""
input_A4 = """I’d like to reserve a table for tomorrow, it’s my mom’s birthday."""
input_A5 = """Do you open next Monday?"""
input_A6 = """Can you please cancel my reservation?"""
inputs_skill = [input_A1, input_A2, input_A3, input_A4, input_A5, input_A6]

# Function test for getting a skill
target_skill = getSkill(skills_skill, examples_skill) 
for i in range(len(inputs)):
    print("# Test", i + 1)
    print("Input:", inputs_skiill[i])
    print("Output:", target_skill(inputs_skill[i]), "\n")

# Context
context_1 = """skill = FoodOrdering"""
context_2 = """skill = FoodOrdering"""
context_3 = """skill = FoodOrdering"""
context_4 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
context_5 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
context_6 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
context_7 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza", "quantity": "2"}]"""
context_8 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza", "quantity": "2"}]"""
contexts = [context_1, context_2, context_3, context_4, context_5, context_6, context_7, context_8]

# User inputs for getting a slot
input_B1 = """Sandwich"""
input_B2 = """Fenta"""
input_B3 = """Three chicken wings, please."""
input_B4 = """Can I change it to Greek Pizza?"""
input_B5 = """Can I get a different pizza, please?"""
input_B6 = """One is enough"""
input_B7 = """Can I also get one more Smoked Chicken Pizza, please?"""
input_B8 = """Grilled Shrimp"""
inputs_slot = [input_B1, input_B2, input_B3, input_B4, input_B5, input_B6, input_B7, input_B8]

# Function test for getting a slot
target_slot = getSlot(types_slot, skills_slot, examples_slot)

for i in range(len(inputs)):
    print("# Test", i + 1)
    print("Context:", contexts[i])
    print("Input:", inputs_slot[i])
    print("Output:", target_slot(inputs_slot[i], contexts[i]), "\n")
