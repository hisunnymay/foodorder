import os
import openai
import foodorder
import json # is used to compare result


# type list
types =  """
Dish
- The dishes that this restaurant supplies.
- Options:
    - Appetizer: Appetizer
        - BuffaloStyleChickenEggRolls: Buffalo Style Chicken Egg Rolls 
        - GrilledShrimp: Grilled Shrimp  
        - ChickenWings: Chicken Wings
    
    - Pizza: Pizza
        - SmokedChickenPizza: Smoked Chicken Pizza
        - GreekPizza: Greek Pizza
        - ItalianPizza: Italian Pizza  
    
    - Sandwich: Sandwich
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

# skill list
skills =  """
"FoodOrdering":
- dishList: the list of dishes
  - Type: DishList

"SlotUpdate":
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
# Inputs valid node entity
example_1 = """
[context]: "{
    "targetSkill": "FoodOrdering"
}"
[input]: "Pizza"
[Analysis]: "The target skill is 'FoodOrdering', and the user inputs 'Pizza'. 'Pizza' is a sub-value of 'Dish', so the dish value can be 'Pizza'. Since there are sub-values under 'Pizza', it's not the leaf value and 'leaf' should be false."
{
	"dishList": [{
		"dish": {
			"value": "Pizza",
			"leaf": false
		}
	}]
}
"""

# Inputs invalid leaf entity
example_2 = """
[context]: "{
    "targetSkill": "FoodOrdering"
}"
[Input]: "Chicken Sandwich"
[Analysis]: "The user inputs 'Chicken Sandwich' and it's a sub-value of 'Dish', so this value is invalid. Since it's not a valid value, we don't need to add the 'leaf' key."
{
	"dishList": [{
		"dish": {
			"value": "Invalid"
		}
	}]
}
"""

# Inputs valid leaf entity
example_3 = """
[context]: "{
    "targetSkill": "FoodOrdering"
}"
[Input]: "Italian Pizza"
[Analysis]: "The user inputs 'Italian Pizza' and it's a sub-value of 'Dish', so the dish value is 'ItalianPizza'. Since there is no sub-value under 'Italian Pizza, it's the leaf value and 'leaf' should be true."
{
	"dishList": [{
		"dish": {
			"value": "ItalianPizza",
			"leaf": true
		}
	}]
}
"""

# Inputs valid leaf entity with quantity
example_4 = """
[context]: "{
    "targetSkill": "FoodOrdering"
}"
[Input]: "Two Italian Pizzas, please"
[Analysis]: "The user mentions 'Italian Pizza' and it's a sub-value of 'Dish', so the dish value is 'ItalianPizza'. The user mentions the quantity of this dish, so its quantity should be 2."
{
	"dishList": [{
		"dish": {
			"value": "ItalianPizza",
			"leaf": true
		},
		"quantity": "2"
	}]
}
"""

# Inputs the quantity of dish
example_5 = """
[Context]: "{
	"targetSkill": "FoodOrdering",
	"pickedSkill": "FoodOrdering"
}"
[Input]: "I'd like two."
[Analysis]: "Since the user only mentions a number, it is assumed that the number refers to the quantity of dish. 
From the user input, the name of dish is not mentioned, so only quantity slot can be filled."
{
	"dishList": [{
		"quantity": "2"
	}]
}
"""

# Slot update: change dish without quantity
example_6 = """
[Context]: "{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"       
[Input]: "Can I swap my Fish Sandwich for something else, please?
[Analysis]: "The target skill is 'SlotUpdate', and the user asks to change 'Fish Sandwich', so 'Fish Sandwich' should be the old value.
As the user doesn't mention the new value, the new value can't be filled."
{
    "originalSlot": "dishList.dish", 
    "oldValue": {
        "value": "FishSandwich",
        "leaf": true
    }
}
"""

# Slot update: change the quantity of dish
example_7 = """
[Context]: "{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"
[Input]: "Can I change to 4?"
[Analysis]: "The target skill is 'SlotUpdate', based on the user's mention of a certain number, and the fact that the quantity aligns with that number, it can be concluded that the quantity is 4."
{
    "originalSlot": "dishList.quantity", 
    "newValue": 4
}
"""

# Slot update: change the quantity of dish without the actual number
example_8 = """
[Context]: "{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"
[Input]: "Three more please"
[Analysis]: "The target skill is 'SlotUpdate', the user asks to add 3 more, so we increase the old value by three to arrive at the new value."
{
    "originalSlot": "dishList.quantity", 
    "newValue": "quantity.plus(3)"
}
"""

examples = example_1 + example_2 + example_3 + example_4 + example_5 + example_6 + example_7 + example_8

# The section presents sets of contexts(e.g. c1), user inputs(e.g. u1) and expected result (e.g. e1).
# When there is no dish selected, inputs the first valid dish without indicating its quantity.
c1 = """{
    "targetSkill": "FoodOrdering"
}"""
i1 = """Sandwich"""
e1 = """{
	"dishList": [{
		"dish": {
			"value": "Sandwich",
			"leaf": false
		}

	}]
}"""

# When there is no dish selected, inputs the first invalid dish without indicating its quantity.
c2 = """{
    "targetSkill": "FoodOrdering"
}"""
i2 = """Fenta"""
e2 = """{
	"dishList": [{
		"dish": {
			"value": "Invalid"
		}
	}]
}"""

# When there is no dish selected, inputs the first valid dish with indicating its quantity.
c3 = """{
    "targetSkill": "FoodOrdering"
}"""
i3 = """Three chicken wings, please."""
e3 = """{
	"dishList": [{
		"dish": {
			"value": "ChickenWings",
			"leaf": true
		},
		"quantity": "3"
	}]
}"""

# When one dish has been selected but not assigned a quantity, asks to replace the currently selected dish with a new one, without specifying the quantity.
c4 = """{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"""
i4 = """Can I change to Greek Pizza?"""
e4 = """{
    "originalSlot": "dishList.dish",
    "newValue": {
        "value": "GreekPizza",
        "leaf": true
    }
}"""

# When one dish has been selected but not assigned a quantity, asks to replace the currently selected dish without specifying the new one and the old one.
c5 = """{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"""
i5 = """Can I switch from the Smoked Chicken Pizza to the Italian Pizza instead, please?"""
e5 = """{
    "originalSlot": "dishList.dish",
    "oldValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    },
    "newValue": {
        "value": "ItalianPizza",
        "leaf": true
    }
}"""

# When one dish has been selected but not assigned a quantity, provides the quantity of the currently selected dish.
c6 = """{
	"targetSkill": "FoodOrdering",
	"pickedSkill": "FoodOrdering"
}"""
i6 = """One is enough"""
e6 = """{
	"dishList": [{
		"quantity": "1"
	}]
}"""

# When one dish has been selected with an assigned quantity, asks to change the quantity of the currently selected dish.
c7 = """{
	"targetSkill": "SlotUpdate",
	"pickedSkill": "FoodOrdering"
}"""
i7 = """Can I also get one more Smoked Chicken Pizza, please?"""
e7 = """{
    "originalSlot": "dishList", 
    "newValue": [{
        "dish": "SmokedChickenPizza", 
        "quantity": "quantity.plus(1)"
    }]
}"""

# When one dish has been selected with an assigned quantity, inputs the second valid dish without indicating its quantity.
c8 = """{
	"targetSkill": "FoodOrdering",
	"pickedSkill": "FoodOrdering"
}"""
i8 = """Grilled Shrimp"""
e8 = """{
	"dishList": [{
		"dish": {
			"value": "GrilledShrimp",
			"leaf": true
		}
	}]
}"""

inputs = [i1, i2, i3, i4, i5, i6, i7, i8]
contexts = [c1, c2, c3, c4, c5, c6, c7, c8]
expected_results = [e1, e2, e3, e4, e5, e6, e7, e8]

# Function test
target_slot = getSlot(types, skills, examples)

for i in range(len(inputs)):
    output = target_slot(inputs[i], contexts[i])
    print("# Test", i + 1, "----------------------------")
    print("Context:", contexts[i])
    print("Input:", inputs[i])
    print("Output:", output, "\n")

    # Compare the output with expected output
    expected_output = json.loads(expected_results[i])
    actual_output = json.loads(output)
    if actual_output == expected_output:
        print("Result: Passed. \n")
    else:
        print("Result: Failed. \nExpected output is: \n", expected_output, "\n")
