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


# There is no reason to have skill model to be in json.
class getSkill:
    def __init__(self, skills, examples):
        self.skills = skills
        self.examples = examples

    def __call__(self, input):
        prompt = f"""
        Given the user input, your task is to determine which of these skills can be implied by it. 
        ```{self.skills}```
        
        For example:
        ```{self.examples}```

        input: ```{input}```
        """
        return get_completion(prompt)


class getSlot:
    def __init__(self, types, skills, slots, examples):
        self.types = types
        self.skillDisc = skills
        self.slotInfo = slots
        self.examples = examples

    def __call__(self, input, context):
        prompt = f"""
        Based on the context, your task is to identify value for following slots from the user input,
        assume the current skill is ```{self.skillDisc}```\
        ```{self.slotInfo}```
        
        Here are some examples:
        ```{self.examples}```
        
        If the slot has a specific type, you should check \
        whether its type is an entity or a frame. Entities have no slots, while frames do.
        - If it's an entity, check whether the user's input matches \
        the candidate values of that type before filling in the slot. \
        If there is no match, then set the slot's value to "Invalid".
        - If it's a frame, fill its slot with the user-input value. 
    
        Format your response as a JSON object with the skill and \
        the user-mentioned slot as the keys.
        Make sure all the value in the JSON object is not null.
        
        Types: ```{self.types}``` 
        
        Context: ```{context}```
        User input: ```{input}```
        """
        return get_completion(prompt)
