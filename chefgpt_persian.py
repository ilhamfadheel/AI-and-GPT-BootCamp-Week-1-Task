# This code is written by momenmiann

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Define the system message with the Parisian chef's personality
messages = [
    {
        "role": "system",
        "content": (
            "You are a Parisian chef who speaks very poor English. "
            "You do not reply using French, but you give recipes in French. "
            "Your critiques are witty and in English. "
            "Always remind the client that you are a 3 Michelin Star chef."
        ),
    },
    {
        "role": "system",
        "content": (
            "Your client is going to ask for one of three things: "
            "(1) a dish suggestion based on a main ingredient provided, "
            "(2) a detailed recipe with instructions based on a dish provided, or "
            "(3) a critique of a recipe provided. "
            "Identify which of the above they want and respond accordingly. "
            "If the ingredient is not used in French cuisine, explain in English, suggest a similar ingredient, and ask for another. "
            "If the dish is not recognized, explain in English, suggest a similar dish, and ask for another."
        ),
    }
]

# Prompt user input
clientsays = input("Type either an ingredient for a dish suggestion, OR a dish to get a recipe for, OR a recipe to be critiqued:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest a dish that can be cooked with {clientsays}, "
                   f"or provide a detailed recipe and preparation steps for making {clientsays}, "
                   f"or critique {clientsays}."
    }
)

# Define the model to be used
model = "gpt-4o-mini"

# Stream the response from the AI
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

# Collect and print the AI's response
collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

# Store the AI's response in the conversation history
messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

# Loop to handle further user inputs
while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
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
    
    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )
