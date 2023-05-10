import os
import openai

openai.api_key = "sk-"  # your openai api key.

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


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


class getSkill:
    def __init__(self, skills, examples):
        self.skills = skills
        self.examples = examples

    def __call__(self, input):
        prompt = f"""
        Given the user input, your task is to determine which of these skills can be implied by it. 
    
        Format your response as a JSON object with "skill" as the key. 
        Here are ```{self.examples}``` you can learn from. 

        Skills: ```{self.skills}```
        User input: ```{input}```
        """
        return get_completion(prompt)


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
        If there is no match, then set the slot's value to "Invalid".
        - If it's a frame, fill its slot with the user-input value. 
    
        Format your response as a JSON object with the skill and \
        the user-mentioned slot as the keys.
        Here are ```{self.examples}``` you can learn from. \
        Make sure all the value in the JSON object is not null.
        
        Context: ```{context}```
        Skills: ```{self.skills}```
        Types: ```{self.types}```
        User input: ```{input}```
        """

        return get_completion(prompt)
