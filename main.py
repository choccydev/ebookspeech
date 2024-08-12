import os
import openai
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Set your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def sentiment_analysis(text):
    """Analyze the sentiment of the provided text using OpenAI's chat completions API"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {
                "role": "user",
                "content": f"Analyze the sentiment of this text: '{text}'.",
            },
        ],
    )
    sentiment = response["choices"][0]["message"]["content"].strip().lower()
    return sentiment


def add_expression_marks(text, sentiment):
    """Add expression marks based on sentiment"""
    expression_marks = {"positive": "😊", "neutral": "😐", "negative": "😠"}
    mark = expression_marks.get(sentiment, "")

    # Append the mark to each sentence.
    sentences = re.split(r"(\.|!|\?)", text)
    processed_sentences = [sentence + mark for sentence in sentences if sentence]

    # Reconstruct the text with expression marks.
    processed_text = "".join(processed_sentences)
    return processed_text


def process_text_with_sentiment_analysis(text):
    sentiment = sentiment_analysis(text)
    processed_text = add_expression_marks(text, sentiment)
    return processed_text


# Example usage
text = "This is a fantastic day. I am so happy to be learning new things. However, there is a lot of work to do."

processed_text = process_text_with_sentiment_analysis(text)
print(processed_text)
