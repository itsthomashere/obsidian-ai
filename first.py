import os
import sys
from pathlib import Path
from typing import List

import assemblyai as aai
import dotenv
import openai
import pendulum


def find_unprocessed_files(station_1_dir: Path, station_2_dir: Path) -> List[str]:
    """
    Compare filenames in station-1--audio-files and station-2--rough-transcripts.
    Return a list of filenames from station-1--audio-files that are missing in station-2--rough-transcripts.
    """

    # Gather all the file names from station-1 and station-2 directories
    # station_1_files = [f.stem.split()[-1] for f in station_1_dir.glob("*.webm" or "*.m4a")]
    station_1_files = [f.stem.split()[-1] for f in station_1_dir.glob("*.webm")]

    station_2_files = [f.stem.split()[-1] for f in station_2_dir.glob("*.md")]

    print(f"In total, there are {len(station_1_files)} audio recordings in station 1")

    # Find the files that are in station-1 but not in station-2
    missing_files = [
        f"Recording {timestamp}.webm"
        for timestamp in station_1_files
        if timestamp not in station_2_files
    ]

    return sorted(missing_files)


def transcribe_audio_file(audio_url: str) -> str:
    """Transcribes audio using AssemblyAI."""
    print("AI: Processing audio...")
    transcript = aai.Transcriber().transcribe(audio_url)
    return transcript.text


if __name__ == "__main__":
    dotenv.load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_TOKEN")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    base_path = Path("./stations")
    station_1_path = base_path / "station-1--audio-files"
    station_2_path = base_path / "station-2--rough-transcripts"

    # Get the list of unprocessed files
    unprocessed_files = find_unprocessed_files(station_1_path, station_2_path)

    if unprocessed_files:
        print(
            "The following rough transcripts are missing in station-2--rough-transcripts:"
        )
        for file in unprocessed_files:
            print(f"- {file}")
        print(f"Number of unprocessed files: {len(unprocessed_files)}")
    else:
        print("All audio recordings have corresponding rough transcripts in station 2.")

    for file in unprocessed_files:
        transcript = transcribe_audio_file(f"{station_1_path}/{file}")
        timestamp = file.split()[-1].replace(".webm", "")
        transcript_filename = station_2_path / f"Rough Transcript {timestamp}.md"
        with open(transcript_filename, "w") as f:
            f.write(transcript)
            print(f"Saving Rough Transcript {timestamp} to {station_2_path}.")
