import os
import openai
import foodorder


# type list
types = """
Dish
- Appetizer
   - BuffaloStyleChickenEggRolls: Buffalo Style Chicken Egg Rolls 
   - GrilledShrimp: Grilled Shrimp  
   - ChickenWings: Chicken Wings
  
- Pizza
  - SmokedChickenPizza: Smoked Chicken Pizza
  - GreekPizza: Greek Pizza
  - ItalianPizza: Italian Pizza  
  
- Sandwich
  - FishSandwich: Fish Sandwich
  - MeatballSandwich: Meatball Sandwich
  - CheesesteakSandwich: Cheesesteak Sandwich
  
DishList
- Description: the list that stores all the dishes that the user has ordered
- Slots
  - dish: the label of the dish
  - quantity: the quantity of this dish
"""

# Skill list
# For getting a skill
skills_skill = """
- ShowHours
  - Description: Show business hours
  - User input example: When do you open?

- MakeReservation
  - Description: Make reservation
  - User input example: I'd like to reserve a table, please.

- CancelReservation
  - Description: Cancel reservation
  - User input example: Sorry, but I need to cancel my reservation.

- ViewReservation
  - Description: Display reservation
  - User input example: Could you show me details of my reservation?

- FoodOrdering
  - Description: Food ordering
  - User input example: Hi there, can I order some food?
"""

simple_skills = """
- ShowHours: Show business hours
- MakeReservation: Make reservation
- CancelReservation: Cancel reservation
- ViewReservation: Show my reservation
- FoodOrdering: Food ordering
- SlotUpdate: Change slot value
"""

simple_skill_examples = """
input: When do you open?
skill: ShowHours
input: I'd like to reserve a table, please.
skill: MakeReservation 

input: Sorry, but I need to cancel my reservation.
skill: CancelReservation 

input: Could you show me details of my reservation?
skill: ViewReservation

input: Hi there, can I order some pizza?
skill: FoodOrdering 

input: I like to change some thing
skill: SlotUpdate
"""

# Examples should be dictionary keyed on skill.
slots = {
    "FoodOrdering": """
    - dishList: the list of dishes
    """,

    "SlotUpdate": """
    - originalSlot: original slot
    - oldValue: old value
    - index: index
    - newValue: new value
    """
}

# For getting a slot
skills_slot = """
FoodOrdering
- Description: Food ordering
- User input example: Hi there, can I order some food?
- Slots
  - dishList: the list of dishes
    - Type: DishList

SlotUpdate: update slot value
- originalSlot: original slot
- oldValue: old value
- index: index
- newValue: new value
"""

# Examples
# For getting a skill
examples_skill = """
[input]: "When do you oepn tomorrow?"
You should respond with: {"skill": "ShowHours"}
    
[input]: "How is the weather?"
You should respond with: {"skill": ""}
"""

# For getting a slot
examples_slot = """
[Context]: "skill = FoodOrdering"
[Input]: "Chicken Sandwich"
{
    "skill": "FoodOrdering", 
    "dishList" = [
    {
        "dish": "Invalid"
    }]
}
[context]: "skill = FoodOrdering"
[input]: "Pizza"
[Input]: "Italian Pizza"
{
    "skill": "FoodOrdering", 
       "dishList" = [
    {
        "dish": "Pizza"
    }]
}

[Context]: "skill = FoodOrdering"
[Input]: "Italian Pizza"
{
    "skill": "FoodOrdering", 
       "dishList" = [
    {
        "dish": "ItalianPizza"
    }]
}

[Context]: "skill = FoodOrdering"
[Input]: "Two Italian Pizzas, please"
{
    "skill": "FoodOrdering", 
    "dishList" = [
    {
        "dish": "ItalianPizza", 
        "quantity": "2"
    }]
}

[Context]: "skill = FoodOrdering, dishList = [{"dish": "FishSandwich"}]"
[Input]: "Can I change it to Meatball Sandwich?"
{
    "skill": "SlotUpdate", 
    "originalSlot" = "dish", 
    "oldValue" = "FishSandwich",
    "newValue": "MeatballSandwich"
}

[Context]: "skill = FoodOrdering, dishList = [{"dish": "FishSandwich", "quantity": "2"}]"
[Input]: "Can I change it to 4?"
{
    "skill": "SlotUpdate", 
    "originalSlot" = "dish", 
    "oldValue" = "FishSandwich",
    "newValue": "MeatballSandwich"
}
"""




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
