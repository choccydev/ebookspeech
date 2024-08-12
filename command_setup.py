import typer
import os


def command_setup():
    """Interactively prompt for OpenAI API key and store it in a .ebookspeech.env file."""
    env_file = ".ebookspeech.env"

    if os.path.exists(env_file):
        typer.echo(f"{env_file} already exists.")
        overwrite = typer.prompt("Do you want to overwrite it? (y/n)", default="n")
        if overwrite.lower() != "y":
            typer.echo("Setup aborted.")
            return

    api_key = typer.prompt("Enter your OpenAI API key")
    with open(env_file, "w") as file:
        file.write(f"OPENAI_API_KEY={api_key}\n")

    typer.echo(f"API key has been saved to {env_file}.")
