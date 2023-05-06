import os
import openai

openai.api_key = "sk-"  # your openai api key.


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def getSkill(user_input, dialog_states, bot_context):
    return ""


def getSlot(user_input, skill_details):
    return ""