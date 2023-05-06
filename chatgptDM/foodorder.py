import os
import openai

openai.api_key = "sk-"  # your openai api key.

menu = """
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 1.00, 2.00, 3.00 \
sprite 3.00, 4.00, 5.00 \
bottled water 5.00 \
"""

instruction =  """
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
Finally you collect the payment.\
If it's a delivery, you ask for an address. \
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
"""

# Notice the chat completion can complete both assist and user, so if you do not pad an empty user message,
# the api will try to complete user as well.
# if you want to try different system prompt, you can also encode the test case here. so that you do not
# need type it in over and over.

conversation = [
    {"role": "system", "content": f"""{instruction}{menu}""" },
    {"role": "user", "content": "hi"}   # This is important so that completion does not run to stop.
]

while(True):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=0  # Try to as deterministic as possible.
    )
    reply = response.choices[0].message["content"]
    print("\nBot:" + reply + "\nUser:")
    conversation.append({"role": "assistant", "content": reply})
    user_input = input()
    conversation.append({"role": "user", "content": user_input})