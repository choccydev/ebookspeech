import json
from tiktoken import Encoding, get_encoding

# Placeholder for model cost (Example values, you can replace these with actual costs)
TOKEN_COST_PER_1000 = (
    0.00015  # Example cost for text processing (e.g., $0.0005 per 1000 tokens)
)
CHAR_COST_PER_1000 = 0.015  # Example cost for TTS (e.g., $0.02 per 1000 characters)


def load_segmented_json(json_file):
    """Load the segmented text from a JSON file."""
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []


def estimate_cost_for_text_processing(segments):
    """Estimate the cost for text processing using token count."""
    tokenizer = get_encoding("cl100k_base")  # Assuming GPT-4 tokenizer

    total_tokens = 0

    for segment in segments:
        tokens = tokenizer.encode(segment)
        total_tokens += len(tokens)

    # Double the token count for processing
    total_tokens *= 2

    # Estimate cost
    estimate_cost = (total_tokens / 1000) * TOKEN_COST_PER_1000
    return estimate_cost


def estimate_cost_for_tts(segments):
    """Estimate the cost for TTS using character count."""
    total_characters = 0

    for segment in segments:
        total_characters += len(segment)

    # Estimate cost
    estimate_cost = (total_characters / 1000) * CHAR_COST_PER_1000
    return estimate_cost


def estimate_costs(json_file):
    segments = load_segmented_json(json_file)
    text_processing_cost = estimate_cost_for_text_processing(segments)
    tts_cost = estimate_cost_for_tts(segments)
    return text_processing_cost, tts_cost


# Example function to demonstrate usage
def example_usage():
    json_file = "segmented_text.json"
    text_cost, tts_cost = estimate_costs(json_file)
    print(f"Estimated cost for text processing: ${text_cost:.4f}")
    print(f"Estimated cost for TTS: ${tts_cost:.4f}")


if __name__ == "__main__":
    example_usage()
