import os
import openai

openai.api_key = "sk-"  # your openai api key.


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
        Based on the skills, your task is to determine which of these skills \
        can appropriately handle the user input. 
    
        You only need to respond with the label of the skill.
        Here are ```{self.examples}``` you can learn from. 

        Skills: ```{self.skills}```
        User input: ```{input}```
        """
        return get_completion(prompt)
    

class getSlot:
    def __init__(self, types, examples):
        self.types = types
        self.examples = examples
    def __call__(self, input, targetSkill, targetSlots):
        prompt = f"""
        Your task is to find values for each slot in the target skill from the user input.
        Target skill is: ```{targetSkill}```.
        The slots to be filled are: ```{targetSlots}```.
        
        If the slot has a specific type, you should check whether its type is an entity or a frame. Entities have no slots, while frames do.
        - If it's an entity, check whether the user's input matches the sub-values of that type before filling in the slot. 
            - There are two kinds of entity values: node and leaf. Node values have sub-values, while leaf values do not.
            - If the user-input value is not a sub-value for that particular entity, then the slot's value should be set to 'Invalid'.
        - If it's a frame, fill its slot with the user-input value. 
    
        Format your response as a JSON object with the label of slots in the target skill as the keys.
        Here are some examples: ```{self.examples}```
        
        Once you've composed your response, before output it, please verify the following:
        - Your reply shoule be a JSON object. Do NOT include your analysis in the response.
        - Collect all the labels of slots in the target skill and all the keys in your response. Every key must be one of those labels. Delete non-matching keys.
        - All values included within the JSON object are non-null.

        
        Types: ```{self.types}```
        User input: ```{input}```
        """
    
        return get_completion(prompt)
