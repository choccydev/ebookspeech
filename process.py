import os
import openai
from dotenv import load_dotenv
import re
import json
from pathlib import Path

# Load environment variables from .ebookspeech.env file
load_dotenv(dotenv_path=".ebookspeech.env")

# Set your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def sentiment_analysis(text):
    """Analyze the sentiment of the provided text using OpenAI's chat completions API."""
    prompt = (
        "Analyze the sentiment of this text and add expression marks based on sentiment. "
        "Ignore TOCs, lists, page numbers, and any other elements that might disturb the reading experience: "
        f"'{text}'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    sentiment = response["choices"][0]["message"]["content"].strip().lower()
    return sentiment


def add_expression_marks(text, sentiment):
    """Add expression marks based on sentiment."""
    expression_marks = {"positive": "😊", "neutral": "😐", "negative": "😠"}
    mark = expression_marks.get(sentiment, "")

    # Append the mark to each sentence
    sentences = re.split(r"(\.|!|\?)", text)
    processed_sentences = [sentence + mark for sentence in sentences if sentence]

    # Reconstruct the text with expression marks
    processed_text = "".join(processed_sentences)
    return processed_text


def process_text_with_sentiment_analysis(text):
    sentiment = sentiment_analysis(text)
    processed_text = add_expression_marks(text, sentiment)
    return processed_text


def process_json_file(input_json_file, output_json_file):
    """Load strings from the JSON file, process them, and save the updated JSON file."""
    try:
        with open(input_json_file, "r") as file:
            data = json.load(file)

        processed_data = [
            process_text_with_sentiment_analysis(segment) for segment in data
        ]

        with open(output_json_file, "w") as file:
            json.dump(processed_data, file)

        print(f"Processing complete. Updated JSON file saved as {output_json_file}.")
    except Exception as e:
        print(f"Error processing JSON file: {e}")


def generate_audio_from_json(json_file):
    """Generate audio files from the JSON file using OpenAI's TTS endpoint."""
    output_directory = ".ebookspeech"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        for index, text in enumerate(data):
            response = openai.Audio.create(model="tts-1", voice="alloy", input=text)

            audio_file_path = Path(output_directory) / f"{index}.opus"
            response.stream_to_file(audio_file_path)

        print(f"Audio generation complete. Files saved in {output_directory}.")
    except Exception as e:
        print(f"Error generating audio: {e}")


# Example function to demonstrate usage
def example_usage():
    input_json_file = "segmented_text.json"
    output_json_file = "ebookspeech_ok.json"
    process_json_file(input_json_file, output_json_file)
    generate_audio_from_json(output_json_file)


if __name__ == "__main__":
    example_usage()
