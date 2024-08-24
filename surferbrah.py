from openai import OpenAI
import re

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "Yo dude, you're like, this totally gnarly chef from the sunny shores of Cali, you know? You're all about that farm-to-table freshness, but you explain it in the chillest way possible. Everything's 'rad,' 'tubular,' or 'far out.' You're always stoked to drop some culinary knowledge, but you do it while hangin' ten in the kitchen, bro. Keep it coastal, keep it cool, and remember - cooking's just like catching waves, you gotta go with the flow!",
    },
    {
        "role": "system",
        "content": "Handle three types of inputs: 1) Ingredient lists, 2) Dish names, 3) Recipes for critique. For ingredient inputs: Suggest only dish names without full recipes. For dish name inputs: Provide a detailed recipe. For recipe inputs: Offer a constructive critique with suggested improvements. If the input doesn't match these scenarios, politely decline and prompt for a valid request.",
    }
]

model = "gpt-4-turbo-preview"

def get_completion(messages):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)
    return "".join(collected_messages)

def identify_input_type(user_input):
    if re.search(r'\b(recipe|ingredients|instructions)\b', user_input, re.IGNORECASE):
        return "recipe"
    elif ',' in user_input or 'and' in user_input:
        return "ingredients"
    else:
        return "dish"

def handle_input(user_input):
    input_type = identify_input_type(user_input)
    
    if input_type == "ingredients":
        prompt = f"Yo bro, check out these rad ingredients: {user_input}. What gnarly dishes can I whip up with these? Just gimme the names of 3-5 dishes, no recipes! Keep it short and sweet, dude!"
    elif input_type == "dish":
        prompt = f"Dude, {user_input} sounds totally tubular! Can you break down the recipe for me, step by step? Make it sound like we're cookin' up a storm on the beach!"
    elif input_type == "recipe":
        prompt = f"Alright, surf's up for this recipe: {user_input}. Let's critique it and make it even more radical. What tweaks can we make to take it to the next level?"
    else:
        return "Whoa there, dude! I'm not pickin' up what you're puttin' down. Can you try again with some ingredients, a dish name, or a recipe to critique?"

    messages.append({"role": "user", "content": prompt})
    response = get_completion(messages)
    messages.append({"role": "assistant", "content": response})
    return response

print("Yo dude, what kinda radical grindage are you lookin' to whip up? Gimme the 411 on the tasty waves you wanna ride in the kitchen, brah!")

while True:
    user_input = input("\nYour input, bro (or type 'exit' to catch the last wave out): ")
    if user_input.lower() == 'exit':
        print("Catch you on the flip side, dude! Stay gnarly!")
        break
    response = handle_input(user_input)
    print("\n")
