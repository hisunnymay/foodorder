import os
import openai

openai.api_key = "sk-"  # your openai api key.

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
skills_skill =  """
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

# For getting a slot
skills_slot =  """
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
# Inputs valid node entity
example_1 = """
[context]: "skill = FoodOrdering"
[input]: "Pizza"
[Analysis]: "The user inputs 'Pizza' and it's in the options of 'Dish', so the dish value can be 'Pizza'. Since there are options under 'Pizza', it's not the leaf value and 'leaf' should be false."
{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "Pizza",
                "leaf": false
            }
        }
    ]
}
"""

# Inputs invalid leaf entity
example_2 = """
[Context]: "skill = FoodOrdering"
[Input]: "Chicken Sandwich"
[Analysis]: "The user inputs 'Chicken Sandwich' and it's not in the options of 'Dish', so this value is invalid. Since it's not a valid value, we don't need to add the 'leaf' key."
{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "Invalid"
            }
        }
    ]
}
"""

# Inputs valid leaf entity
example_3 = """
[Context]: "skill = FoodOrdering"
[Input]: "Italian Pizza"
[Analysis]: "The user inputs 'Italian Pizza' and it's in the options of 'Dish', so the dish value is 'ItalianPizza'. Since there is no option under 'Italian Pizza, it's the leaf value and 'leaf' should be true."
{
    "skill": "FoodOrdering", 
    "dishList": [
        {
            "dish": {
                "value": "ItalianPizza",
                "leaf": true
            }
        }
    ]
}
"""

# Inputs valid leaf entity with quantity
example_4 = """
[Context]: "skill = FoodOrdering"
[Input]: "Two Italian Pizzas, please"
[Analysis]: "The user mentions 'Italian Pizza' and it's in the options of 'Dish', so the dish value can be 'ItalianPizza'. The user mentions the quantity of this dish, so its quantity should be 2."
{
    "skill": "FoodOrdering", 
       "dishList": [
        {
            "dish":{
                "value": "ItalianPizza",
                "leaf": true
            },
            "quantity": "2"
        }
    ]
}
"""

# Inputs the quantity of dish
example_5 = """
[Context]: "skill = FoodOrdering, dishList = [{"dish": "FishSandwich"}]"
[Input]: "I'd like two."
[Analysis]: "Since the user only mentions a number and 'FishSandwich' lacks a specific quantity, it is assumed that the number refers to the quantity of 'FishSandwich'."
{
    "skill": "FoodOrdering", 
       "dishList": [
        {
            "dish": "FishSandwich",
            "quantity": "2"
        }
    ]
}
"""

# Slot update: change dish without quantity
example_6 = """
[Context]: "skill = FoodOrdering, dishList = [{"dish": "FishSandwich"}]"
[Input]: "Can I swap my Fish Sandwich for something else, please?
[Analysis]: "The user asks to update the dish and the new dish is in the options of 'Dish', so the skill should be `SlotUpdate`."
{
    "skill": "SlotUpdate", 
    "originalSlot": "dishList.dish", 
    "oldValue": {
        "value": "FishSandwich",
        "leaf": true
    }
}
"""

# Slot update: change the quantity of dish
example_7 = """
[Context]: "skill = FoodOrdering, dishList = [{"dish": "FishSandwich", "quantity": "2"}]"
[Input]: "Can I change it to 4?"
[Analysis]: "The user asks to update the quantity of a dish, so the skill should be `SlotUpdate`. Since the quantity is paired with the dish, the 'originalSlot' should be 'dishList'. \
Since the quantity of the dish is fixed and there are no further options or sub-values for it, we can simply consider it as a 'leaf value' without explicitly adding a 'leaf' key."
{
    "skill": "SlotUpdate", 
    "originalSlot": "dishList", 
    "oldValue": [{"dish": "FishSandwich", "quantity": "2"}],
    "newValue": [{"dish": "FishSandwich", "quantity": "4"}]
}
"""

examples_slot = example_1 + example_2 + example_3 + example_4 + example_5 + example_6 + example_7

# Call ChatGPT API
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Given user input, figure out which skills it implies. 
class getSkill:
    def __init__(self, skills, examples): 
        self.skills = skills
        self.examples = examples
    def __call__(self, input):
        prompt = f"""
        Based on the skills, your task is to determine which of these skills \
        can appropriately handle the user input. 
    
        Format your response as a JSON object with "skill" as the key. 
        Here are ```{examples}``` you can learn from. 

        Skills: ```{skills}```
        User input: ```{input}```
        """
        return get_completion(prompt)

# Given user input and picked skill, including the slots of frame with nested entities, figure out which slot(s) to fill.
class getSlot:
    def __init__(self, types, skills, examples): 
        self.types = types
        self.skills = skills
        self.examples = examples
    def __call__(self, input, context):
        prompt = f"""
        Based on the context, your task is to \
        determine which skills can appropriately handle the user input, \
        find the corresponding slot and fill it with the user-input value. 
        
        If the slot has a specific type, you should check \
        whether its type is an entity or a frame. Entities have no slots, while frames do.
        - If it's an entity, check whether the user's input matches \
        the candidate values of that type before filling in the slot. \
          - There are two kinds of entity values: node and leaf. Node values have sub-values or options, while leaf values do not.
          - If the user-input value is not listed as one of the options for that particular entity, then the slot's value should be set to 'Invalid'.

        - If it's a frame, fill its slot with the user-input value. 
    
        Format your response as a JSON object with the skill and \
        the user-mentioned slot as the keys.
        Here are ```{examples}``` you can learn from. \
        Make sure all the value in the JSON object is not null.
        
        Context: ```{context}```
        Skills: ```{skills}```
        Types: ```{types}```
        User input: ```{input}```
        """
    
        return get_completion(prompt)
