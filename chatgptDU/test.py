import os
import openai
import foodorder
import json # used in comparing actual outputs and expected outputs

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

# The section presents sets of contexts(e.g. c1), user inputs(e.g. u1) and expected result (e.g. e1).
# When there is no dish selected, inputs the first valid dish without indicating its quantity.
c1 = """skill = FoodOrdering"""
i1 = """Sandwich"""
e1 = """{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "Sandwich",
                "leaf": false
            }
            
        }
    ]
}"""

# When there is no dish selected, inputs the first invalid dish without indicating its quantity.
c2 = """skill = FoodOrdering"""
i2 = """Fenta"""
e2 = """{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "Invalid"
            }
        }
    ]
}"""

# When there is no dish selected, inputs the first valid dish with indicating its quantity.
c3 = """skill = FoodOrdering"""
i3 = """Three chicken wings, please."""
e3 = """{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "ChickenWings",
                "leaf": true
            },
            "quantity": "3"
        }
    ]
}"""

# When one dish has been selected but not assigned a quantity, asks to replace the currently selected dish with a new one, without specifying the quantity.
c4 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
i4 = """Can I change it to Greek Pizza?"""
e4 = """{
    "skill": "SlotUpdate",
    "originalSlot": "dishList.dish",
    "oldValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    },
    "newValue": {
        "value": "GreekPizza",
        "leaf": true
    }
}"""

# When one dish has been selected but not assigned a quantity, asks to replace the currently selected dish without specifying the new one and the quantity.
c5 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
i5 = """Can I get a different pizza, please?"""
e5 = """{
    "skill": "SlotUpdate",
    "originalSlot": "dishList.dish",
    "oldValue": {
        "value": "SmokedChickenPizza",
        "leaf": true
    },
    "newValue": {
        "value": "Pizza",
        "leaf": false
    }
}"""

# When one dish has been selected but not assigned a quantity, provides the quantity of the currently selected dish.
c6 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza"}]"""
i6 = """One is enough"""
e6 = """{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": "SmokedChickenPizza", 
            "quantity": "1"
        }
    ]
}"""

# When one dish has been selected with an assigned quantity, asks to change the quantity of the currently selected dish.
c7 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza", "quantity": "2"}]"""
i7 = """Can I also get one more Smoked Chicken Pizza, please?"""
e7 = """{
    "skill": "SlotUpdate", 
    "originalSlot": "dishList", 
    "oldValue": [{"dish": "SmokedChickenPizza", "quantity": "2"}],
    "newValue": [{"dish": "SmokedChickenPizza", "quantity": "3"}]
}"""

# When one dish has been selected with an assigned quantity, inputs the second valid dish without indicating its quantity.
c8 = """skill = FoodOrdering, dishList = [{"dish": "SmokedChickenPizza", "quantity": "2"}]"""
i8 = """Grilled Shrimp"""
e8 = """{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "GrilledShrimp",
                 "leaf": true
            }
        }
    ]
}"""

inputs = [i1, i2, i3, i4, i5, i6, i7, i8]
contexts = [c1, c2, c3, c4, c5, c6, c7, c8]
expected_results = [e1, e2, e3, e4, e5, e6, e7, e8]

# Function test
target_slot = getSlot(types, skills, examples)

for i in range(len(inputs)):
    output = target_slot(inputs[i], contexts[i], expected_results[i])
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
