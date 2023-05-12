import os
import openai
import foodorder
import json # compare result

# Function test for geting a skill -------------------------------
# Skill list
simple_skills = """
- ShowHours: Show business hours
- MakeReservation: Make reservation
- CancelReservation: Cancel reservation
- ViewReservation: Show my reservation
- FoodOrdering: Food ordering
- SlotUpdate: Change slot value
"""

# Examples
simple_skill_examples = """
input: When do you open?
ShowHours

input: I'd like to reserve a table, please.
MakeReservation 

input: Sorry, but I need to cancel my reservation.
CancelReservation 

input: Could you show me details of my reservation?
ViewReservation

input: Hi there, can I order some pizza?
FoodOrdering 

input: I like to change some thing
SlotUpdate

input: How is the weather?
null

input: Could I get two more Chicken Wings, please?
SlotUpdate
"""

# User inputs
input_1 = "Hey there, can I get a coke please?"
input_2 = "What kind of shampoo do you guys carry?"
input_3 = "I wanna check out my reservation."""
input_4 = "I'd like to reserve a table for tomorrow, it's my mom's birthday."
input_5 = "Do you open next Monday?"
input_6 = "Can you please cancel my reservation?"
input_7 = "Can I swap my Fish Sandwich for something else, please??"
inputs = [input_1, input_2, input_3, input_4, input_5, input_6, input_7]

# Function test 
target_skill = foodorder.getSkill(simple_skills, simple_skill_examples) 

print("------------------------------- getSkill ------------------------------- \n")

for i in range(len(inputs)):
    print("# Test", i + 1)
    print("Input:", inputs[i])
    print("Output:", target_skill(inputs[i]), "\n")


# Function test for geting a slot -------------------------------
# Type list
types =  """
DishName
- Description: name of dish
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
  
Dish
- Description: dish
- Slots
    - dishName: name of dish
        - Type: DishName
    - quantity: quantity of dish
"""

# Examples 
example_order = """
Description of skill:
{
    "label": "FoodOrdering",
    "description": "Food Ordering"
}
Slots in that skill:
[{
    "label": "dishes",
    "type": "Dish",
    "description": "dishes"
}]
Input and output: (The analysis is used for you to understand how to get the output)
"""
# 1. Inputs valid node entity
example_order_1 = """
[input]: "Pizza"
[Analysis]: "'Pizza' is a sub-value of 'DishName', so the 'dishName' is 'Pizza'. Since there are sub-values under 'Pizza', it's not the leaf value and 'leaf' should be false."
{
	"dishes": [{
		"dishName": {
			"value": "Pizza",
			"leaf": false
		}
	}]
}

[input]: "Appetizer"
{
	"dishes": [{
		"dishName": {
			"value": "Appetizer",
			"leaf": false
		}
	}]
}
"""

# 2. Inputs invalid leaf entity
example_order_2 = """
[Input]: "Chicken Sandwich"
[Analysis]: "'Chicken Sandwich' is not a sub-value of 'DishName', so this value is invalid. Since it's an invalid value, we don't need to add the 'leaf' key."
{
	"dishes": [{
		"dishName": {
			"value": "Invalid"
		}
	}]
}
"""

# 3. Inputs valid leaf entity
example_order_3 = """
[Input]: "Italian Pizza"
[Analysis]: "'Italian Pizza' is a sub-value of 'DishName', so the dish value is 'ItalianPizza'. Since there is no sub-value under 'Italian Pizza, it's the leaf value and 'leaf' should be true."
{
	"dishes": [{
		"dishName": {
			"value": "ItalianPizza",
			"leaf": true
		}
	}]
}
"""

# 4. Inputs valid leaf entity with quantity
example_order_4 = """
[Input]: "Two Italian Pizzas, please"
[Analysis]: "Italian Pizza' is a sub-value of 'DishName', so the dish value is 'ItalianPizza'. The user mentions the quantity of this dish, so its quantity should be 2."
{
	"dishes": [{
		"dishName": {
			"value": "ItalianPizza",
			"leaf": true
		},
		"quantity": 2
	}]
}
"""

# 5. Inputs the quantity of dish
example_order_5 = """
[Input]: "I'd like two."
[Analysis]: "Since the user only mentions a number, it is assumed that the number refers to the quantity of dish."
{
	"dishes": [{
		"quantity": 2
	}]
}
"""

# Examples for SlotUpdate skill
example_update = """
Description of skill:
{
    "label": "SlotUpdate",
    "description": "It's used to identify the label of which slot needs to be updated, along with its old value, new value and index. The value the of 'originalSlot' slot should be one of the 'candidateValues'."
}
Slots in that skill:
[{
	"label": "originalSlot",
	"description": "The label of which slot needs to be updated.",
	"candidateValues": [{
		"dishes": "dishes"
	}, {
		"dishes.dishName": "name of dish"
	}, {
		"dishes.quantity": "quantity of dish"
	}]
}, {
	"label": "oldValue",
	"description": "The old value the slot"
}, {
	"label": "index",
	"description": "The index of the slot if the slot is an array."
}, {
	"label": "newValue",
	"description": "The new value the slot"
}]
Input and output: (The analysis is used for you to understand how to get the output)
"""

# 1. Update dish name with old value
example_update_1 = """
[Input]: "Can I swap my Fish Sandwich for something else, please?"
[Analysis]: "'Fish Sandwich' is the name of dish, so the value of 'originalSlot' should be 'dishes.dishName'. 
The user asks to change 'Fish Sandwich', so it should be the 'oldValue'. 
No new value mentioned, so 'newValue' should not be included."
{
    "originalSlot": "dishes.dishName", 
    "oldValue": {
        "value": "FishSandwich",
        "leaf": true
    }
}

[Input]: "Do you mind if I exchange the Buffalo Style Chicken Egg Rolls for another item on the menu?"
{
    "originalSlot": "dishes.dishName", 
    "oldValue": {
        "value": "BuffaloStyleChickenEggRolls",
        "leaf": true
    }
}
"""

# 2. Update dish name with new value
example_update_2 = """
[Input]: "Can I change to Cheesesteak Sandwich?"
[Analysis]: "'Cheesesteak Sandwich' is the name of dish, so the value of 'originalSlot' should be 'dishes.dishName'. 
The user asks to change to 'Cheesesteak Sandwich', so it should be the 'newValue'. 
No old value mentioned, so 'oldValue' should not be included."
{
    "originalSlot": "dishes.dishName",
    "newValue": {
        "value": "CheesesteakSandwich",
        "leaf": true
    }
}

[Input]: "Can I get the Smoked Chicken Pizza instead?"
{
    "originalSlot": "dishes.dishName",
    "newValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    }
}

[Input]: "Switch it to Fish Sandwich, please?"
{
    "originalSlot": "dishes.dishName",
    "newValue": {
        "value": "FishSandwich",
        "leaf": true
    }
}

[Input]: "Can you change my order to the Grilled Shrimp?"
{
    "originalSlot": "dishes.dishName",
    "newValue": {
        "value": "GrilledShrimp",
        "leaf": true
    }
}
"""

# 3. Update quantity with new value (actual number)
example_update_3 = """
[Input]: "Can I change to 4?"
[Analysis]: "'4' is the quantity of dish, so the value of 'originalSlot' should be 'dishes.quantity'.
No old value mentioned, so 'oldValue' should not be included.""
{
    "originalSlot": "dishes.quantity", 
    "newValue": 4
}

[Input]: "Switch it to three, please?"
{
    "originalSlot": "dishes.quantity", 
    "newValue": 3
}

[Input]: "Is five okay instead?"
{
    "originalSlot": "dishes.quantity", 
    "newValue": 5
}
"""

# 4. Update quantity with new value (calculation on old value)
example_update_4 = """
[Input]: "Three more please"
[Analysis]: "'3' is the quantity of the dish, so the value of 'originalSlot' should be 'dishes.quantity'. 
As the user needs three more, we increase the old value by three to arrive at the new value. 
The format 'slotLabel.plus(n)' is utilized to encode calculations. 
No old value mentioned, so 'oldValue' should not be included."
{
    "originalSlot": "dishes.quantity", 
    "newValue": "quantity.plus(3)"
}

[Input]: "I'll take two additional ones please"
{
    "originalSlot": "dishes.quantity", 
    "newValue": "quantity.plus(2)"
}

[Input]: "Could you add one more, please?"
{
    "originalSlot": "dishes.quantity", 
    "newValue": "quantity.plus(1)"
}
"""

# 5. Update dish (name and quantity) with new value and old value
example_update_5 = """
[Input]: "Can I actually just get two chicken wings instead? Four might be a bit too much for me."
[Analysis]: "The user mentions both quantity and name of the dish, so the output should be 'originalSlot': 'dishes'.
Since user mentions the both the previous quantity and the new quantity, the 'oldValue' and 'newValue' should be included."
{
    "originalSlot": "dishes", 
    "oldValue": [{
        "dishName": "ChickenWings", 
        "quantity": 4
    }],
    "newValue": [{
        "dishName": "ChickenWings", 
        "quantity": 2
    }]
}

[Input]: "Would it be okay to change my order to one Meatball Sandwich instead? Two might be too heavy for me."
{
    "originalSlot": "dishes", 
    "oldValue": [{
        "dishName": "MeatballSandwich", 
        "quantity": 2
    }],
    "newValue": [{
        "dishName": "MeatballSandwich", 
        "quantity": 1
    }]
}

[Input]: "Can I change the quantity of Chicken Wings from 3 to 2?"
{
    "originalSlot": "dishes", 
    "oldValue": [{
        "dishName": "ChickenWings", 
        "quantity": 3
    }],
    "newValue": [{
        "dishName": "ChickenWings", 
        "quantity": 2
    }]
}
"""

# 6. Update dish (name and quantity) with new value
example_update_6 = """ 
[Input]: "Can I get another Grilled Shrimp, please?"
[Analysis]: "The user mentions both quantity and name of the dish, so the output should be 'originalSlot': 'dishes'.
No old value mentioned, so 'oldValue' should not be included."
{
    "originalSlot": "dishes", 
    "newValue": [{
        "dishName": "GrilledShrimp", 
        "quantity": "quantity.plus(1)"
    }]
}

[Input]: "Could I get two more Chicken Wings, please?"
{
    "originalSlot": "dishes", 
    "newValue": [{
        "dishName": "ChickenWings", 
        "quantity": "quantity.plus(2)"
    }]
}

[Input]: "Can I have an extra Cheesesteak Sandwich?"
{
    "originalSlot": "dishes", 
    "newValue": [{
        "dishName": "CheesesteakSandwich", 
        "quantity": "quantity.plus(1)"
    }]
}
"""

examples = example_order + example_order_1 + example_order_2 + example_order_3 + example_order_4 + example_order_5
examples += example_update + example_update_1 + example_update_2 + example_update_3 + example_update_4 + example_update_5 + example_update_6


# User inputs and expected outputs
skill_order = """{
    "label": "FoodOrdering",
    "description": "Food Ordering"
}"""

slot_order = """[{
    "label": "dishes",
    "type": "Dish",
    "description": "dishes"
}]"""

# Inputs the valid dish without indicating its quantity.
sk_1 = skill_order
sl_1 = slot_order
i1 = """Sandwich"""
e1 = """{
	"dishes": [{
		"dishName": {
			"value": "Sandwich",
			"leaf": false
		}

	}]
}"""

# Inputs the invalid dish without indicating its quantity.
sk_2 = skill_order
sl_2 = slot_order
i2 = """Fenta"""
e2 = """{
	"dishes": [{
		"dishName": {
			"value": "Invalid"
		}
	}]
}"""

# Inputs the valid dish with indicating its quantity.
sk_3 = skill_order
sl_3 = slot_order
i3 = """Three chicken wings, please."""
e3 = """{
	"dishes": [{
		"dishName": {
			"value": "ChickenWings",
			"leaf": true
		},
		"quantity": 3
	}]
}"""

# Inputs the quantity of without indicating its dish.
sk_4 = skill_order
sl_4 = slot_order
i4 = """One is enough"""
e4 = """{
	"dishes": [{
		"quantity": 1
	}]
}"""

# Test SlotUpdate skill
skill_update = """{
    "label": "SlotUpdate",
    "description": "It's used to identify the label of which slot needs to be updated, along with its old value, new value and index. The value the of 'originalSlot' slot should be one of the 'candidateValues'."
}"""
slot_update = """[{
    "label": "originalSlot",
    "description": "The label of which slot needs to be updated.",
    "candidateValues": [{
        "dishes": "dishes"
    }, {
        "dishes.dishName": "name of dish"
    }, {
        "dishes.quantity": "quantity of dish"
    }]
}, {
    "label": "oldValue",
    "description": "The old value the slot"
}, {
    "label": "index",
    "description": "The index of the slot if the slot is an array."
}, {
    "label": "newValue",
    "description": "The new value the slot"
}]"""

# Update dish name with a new one
sk_5 = skill_update
sl_5 = slot_update
i5 = """Can I change to Smoked Chicken Pizza?"""
e5 = """{
    "originalSlot": "dishes.dishName",
    "newValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    }
}"""

# Slot update: Asks to replace the dish with specifying the new one and the old one.
sk_6 = skill_update
sl_6 = slot_update
i6 = """Can I switch from the Smoked Chicken Pizza to the Italian Pizza instead, please?"""
e6 = """{
    "originalSlot": "dishes.dishName",
    "oldValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    },
    "newValue": {
        "value": "ItalianPizza",
        "leaf": true
    }
}"""

# Slot update: Asks to change the quantity of the dish.
sk_7 = skill_update
sl_7 = slot_update
i7 = """Can I actually just get two fish sandwiches instead? Four might be a bit too much for me."""
e7 = """{
    "originalSlot": "dishes", 
    "oldValue": [{
        "dishName": "FishSandwich", 
        "quantity": 4
    }],
    "newValue": [{
        "dishName": "FishSandwich", 
        "quantity": 2
    }]
}"""

skills = [sk_1, sk_2, sk_3, sk_4, sk_5, sk_6, sk_7]
slots = [sl_1, sl_2, sl_3, sl_4, sl_5, sl_6, sl_7]
inputs = [i1, i2, i3, i4, i5, i6, i7]
expected_results = [e1, e2, e3, e4, e5, e6, e7]

# Function test
target_slot = foodorder.getSlot(types, examples)

print("------------------------------- getSlot ------------------------------- \n")

for i in range(len(inputs)):
    output = target_slot(inputs[i], skills[i], slots[i])
    print("# Test", i + 1, "----------------------------")
    # print("Skill:", skills[i])
    # print("Slots:", slots[i])
    print("Input:", inputs[i])
    print("Output:", output, "\n")

    # Compare the output with expected output
    expected_output = json.loads(expected_results[i])
    actual_output = json.loads(output)
    if actual_output == expected_output:
        print("Result: Passed. \n")
    else:
        print("Result: Failed. \nExpected output is: \n", expected_output, "\n")
