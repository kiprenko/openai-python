import sys
from openai import OpenAI
from dotenv import load_dotenv

STRUCTURE_SYSTEM_PROMPT = ("Your are a famous Tech Youtube blogger assistant. "
                           "You help writing scripts for videos. "
                           "The script must contain: "
                           "introduction to the topic of the video;"
                           "the main part structure as a list of up to 5 pts"
                           "outro part that summarises everything and "
                           "gives some recommendations/hints for viewers."
                           "The script must not have any formatting/emoji."
                           "Give the general structure, not the details")

MODEL = "gpt-4.1"
MAX_AMOUNT_OF_PROMPTS = 10


def main():
    load_dotenv()
    client = OpenAI()
    initial_prompt = input("Tell me the idea for your video. "
                           "1-3 sentences is enough: ")
    messages = [
        {
            "role": "system",
            "content": STRUCTURE_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": initial_prompt
        }
    ]

    print_model_response(prompt(client, messages))
    prompts_made = 1
    while prompts_made < MAX_AMOUNT_OF_PROMPTS:
        reprompt = input("Type an additional prompt "
                         "or type quit to exit the program: ")
        if reprompt == "quit" or reprompt == "exit" or reprompt == "q":
            print("Thank you, bye!")
            sys.exit(0)
        messages.append({
            "role": "user",
            "content": reprompt
        })
        print_model_response(prompt(client, messages))
        prompts_made += 1


def prompt(client, messages):
    model_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=512
    ).choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": model_response
    })
    return model_response


def print_model_response(model_response):
    print("AI Ghost writer:\n\n" + model_response + "\n\n")


if __name__ == "__main__":
    main()
