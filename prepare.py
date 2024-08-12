import pypandoc
import json
import typer

app = typer.Typer()


def convert_ebook_to_txt(ebook_path: str, output_txt_file: str):
    """Convert an ebook to a text file using Pandoc."""
    try:
        pypandoc.convert_file(ebook_path, "plain", outputfile=output_txt_file)
        typer.echo(f"Conversion completed: {output_txt_file}")
    except Exception as e:
        typer.echo(f"Error in conversion: {e}")


def segment_text_file(
    input_txt_file: str, output_json_file: str, segment_length: int = 3000
):
    """Segment a text file into JSON containing strings of no more than 3k characters."""
    try:
        with open(input_txt_file, "r") as file:
            text = file.read()

        segments = [
            text[i : i + segment_length] for i in range(0, len(text), segment_length)
        ]

        with open(output_json_file, "w") as json_file:
            json.dump(segments, json_file)

        typer.echo(f"Segmentation completed: {output_json_file}")
    except Exception as e:
        typer.echo(f"Error in segmentation: {e}")
