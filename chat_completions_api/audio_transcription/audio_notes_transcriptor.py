import sys
from openai import OpenAI
from dotenv import load_dotenv

STRUCTURE_SYSTEM_PROMPT = "Your task is to structure and organise " \
                 "transcriptions of audio notes. " \
                 "You accept a transcription and " \
                 "provide it structured in the same language. " \
                 "Do not use Markdown, emoji or any other text formatting. " \
                 "Make the text easy to read, get rid of any vermin words. " \
                 "The result must look like " \
                 "a title and a paragraph with the summary " \
                 "of the given audio note transcription."

TRANSCRIPTION_MODEL = "gpt-4o-transcribe"
STRUCTURE_MODEL = "gpt-4.1"


def main():
    args_count = len(sys.argv)
    if args_count < 2:
        print("Usage: python audio_notes_transcriptor.py <path-to-audio-file>")
        sys.exit(1)
    load_dotenv()
    path_to_audio_file = sys.argv[1]
    audio_file = open(path_to_audio_file, "rb")
    client = OpenAI()

    transcription = transcript(client, audio_file).text
    print("Your audio transcription:\n\n" + transcription + "\n")
    to_structure = input("Do you want to structure it? (yes/no): ")
    if to_structure != "yes" and to_structure != "y":
        print("Bye!")
        sys.exit(0)
    structured_transcript = structure(client, transcription)

    print("Your structured audio transcription:\n\n" + structured_transcript)


def transcript(client, audio_file):
    return client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file
    )


def structure(client, transcription):
    return client.chat.completions.create(
        model=STRUCTURE_MODEL,
        messages=[
            {
                "role": "system",
                "content": STRUCTURE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    ).choices[0].message.content


if __name__ == "__main__":
    main()
