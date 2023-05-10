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


# There is no reason to include to skill in the response, as each getSlot is called
# against one of the skill, so we already know that. We just need to get the slot for that
# skill.
# what is the context for?
class getSlot:
    def __init__(self, types, skills, slots, examples):
        self.types = types
        self.skillDisc = skills
        self.slotInfo = slots
        self.examples = examples

    def __call__(self, input, context):
        prompt = f"""
        Based on the context, your task is to convert user input into structured data. 
        Context is consist of target skill and picked skill.
        
        To get the structured data, you need to follow these steps:
        
        1. In ```{self.skills}```, get the slots of the target skill.
        
        2. Extract value from the user input to fill the slots of the target skill. 
          - If you need to include a calculation, please use the following encoding format: 'slotLabel.plus(n)'.

        3. Check whether the slot has a specific type, if so, you should check whether its type is an entity or a frame. Entities have no slots, while frames do.
          - If it's an entity, check whether the user's input matches the sub-values of that type before filling in the slot. 
            - There are two kinds of entity values: node and leaf. Node values have sub-values, while leaf values do not.
            - If the user-input value is not a sub-value for that particular entity, then the slot's value should be set to 'Invalid'.
          - If it's a frame, fill its slot with the user-input value. 
    
		4. Format your reply as a JSON object, with the slots mentioned by the user used as the keys. 
        Here are some examples: ```{self.examples}```. Do NOT output your analysis.
          
        5. Once you've composed your response, before output it, please verify the following:
 			- Your reply is a JSON object.
			- All values included within the JSON object are non-null.
			- The slots that you have filled come from the target skill. 
        
        Types: ```{self.types}```
        Context: ```{context}```
        User input: ```{input}```
        """
    
        return get_completion(prompt)
