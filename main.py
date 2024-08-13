import typer
from prepare import convert_ebook_to_txt, segment_text_file
from command_setup import command_setup
from process import process_json_file, generate_audio_from_json
from postprocess import stitch_audio_files
from estimate import estimate_costs

from enum import Enum

app = typer.Typer()


class ProcessType(str, Enum):
    text = "text"
    audio = "audio"


@app.command()
def setup():
    """Setup the environment and configuration."""
    command_setup()


@app.command()
def prepare(ebook_path: str):
    """Prepare the text for processing by converting an ebook and segmenting the text.

    Arguments:
    ebook_path -- the path to the ebook file
    """
    output_txt_file = ".ebookspeech.txt"
    output_json_file = "ebookspeech.json"

    typer.echo("Starting ebook conversion to text...")
    convert_ebook_to_txt(ebook_path, output_txt_file)

    typer.echo("Starting text segmentation...")
    segment_text_file(output_txt_file, output_json_file)

    typer.echo(
        f"Preparation complete. Text segmented and stored in {output_json_file}."
    )


@app.command()
def process(process_type: ProcessType, input_json_file: str):
    """Process the text using sentiment analysis.

    Arguments:
    process_type -- the type of processing (e.g., text, audio)
    input_json_file -- the path to the input JSON file
    """
    if process_type == ProcessType.text:
        output_json_file = "ebookspeech_ok.json"
        typer.echo(f"Processing text with sentiment analysis and expression marks...")
        process_json_file(input_json_file, output_json_file)
        typer.echo(
            f"Processing complete. Updated JSON file saved as {output_json_file}."
        )
    elif process_type == ProcessType.audio:
        typer.echo(f"Generating audio from JSON file...")
        generate_audio_from_json(input_json_file)
        typer.echo(f"Audio generation complete.")
    else:
        typer.echo("Unsupported process type.")


@app.command()
def postprocess():
    """Postprocess the text."""
    stitch_audio_files()
    typer.echo("Postprocessing complete. Audiobook generated.")


@app.command()
def estimate(json_file: str):
    """Estimate the cost of processing the text.

    Arguments:
    json_file -- the path to the segmented JSON file
    """
    text_cost, tts_cost = estimate_costs(json_file)
    typer.echo(f"Estimated cost for text processing: ${text_cost:.4f}")
    typer.echo(f"Estimated cost for TTS: ${tts_cost:.4f}")


if __name__ == "__main__":
    app()
