import os
from pydub import AudioSegment


def stitch_audio_files(directory=".ebookspeech", output_file="final_audiobook.opus"):
    """Load audio files from the .ebookspeech directory and stitch them together to form a finalized audiobook."""
    try:
        # Initialize an empty AudioSegment
        final_audio = AudioSegment.empty()

        # Get list of audio files, ensuring they are processed in order
        audio_files = sorted(
            [
                os.path.join(directory, file)
                for file in os.listdir(directory)
                if file.endswith(".opus")
            ],
            key=lambda x: int(os.path.splitext(os.path.basename(x))[0]),
        )

        # Combine audio files
        for audio_file in audio_files:
            audio_segment = AudioSegment.from_file(audio_file)
            final_audio += audio_segment

        # Export the final audio file
        final_audio.export(output_file, format="opus")
        print(f"Audiobook generated successfully and saved as {output_file}")

    except Exception as e:
        print(f"Error while stitching audio files: {e}")


# Example function to demonstrate usage
def example_usage():
    stitch_audio_files()


if __name__ == "__main__":
    example_usage()
