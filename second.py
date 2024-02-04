import os
import dotenv
import ai_tools as ai

from pathlib import Path
import pendulum
from typing import List

def find_unprocessed_transcripts(station_2_dir: Path, station_3_dir: Path) -> List[str]:
    """Return a list of filenames from station-2 that are missing in station-3."""
    
    # Extract timestamps from station-2 file names
    station_2_files = [f.stem.split()[-1] for f in station_2_dir.glob("*.md")]
    
    # Extract timestamps from station-3 file names
    station_3_files = [f.stem.split()[-1] for f in station_3_dir.glob("*.md")]

    # Find missing files
    missing_files = [f"Rough Transcript {timestamp}.md" for timestamp in station_2_files if timestamp not in station_3_files]

    return sorted(missing_files)

if __name__ == "__main__":
    station_2_path = Path("stations/station-2--rough-transcripts")
    station_3_path = Path("stations/station-3--polished-transcripts")

    # Check for unprocessed transcripts and list them
    unprocessed_transcripts = find_unprocessed_transcripts(station_2_path, station_3_path)

    if unprocessed_transcripts:
        print("The following rough transcripts are missing in station-3--polished-transcripts:")
        for file in unprocessed_transcripts:
            print(f"- {file}")
        print(f"Number of unprocessed files: {len(unprocessed_transcripts)}")

    else:
        print("All rough transcripts have corresponding polished transcripts in station 3.")


    for i, file in enumerate(unprocessed_transcripts):
        print(f"Processing file {i+1} of {len(unprocessed_transcripts)}")
        with open(f"{station_2_path}/{file}", "r") as f:
            rough_transcript = f.read()
        refined_transcript = ai.refine_transcript(rough_transcript)

        timestamp = file.split()[-1].replace('.md', '')
        transcript_filename = station_3_path / f"Transcript {timestamp}.md"
        with open(transcript_filename, 'w') as f:
            f.write(refined_transcript.lstrip('"').rstrip('"'))
            print(f"Saving Transcript {timestamp} to {station_3_path}.")

