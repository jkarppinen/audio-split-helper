import argparse
import csv
from datetime import datetime, timedelta
from typing import List

def save_to_file(lines: List[str], filename: str) -> None:
    """Save a list of lines to a file."""
    with open(filename, "w") as f:
        f.write("\n".join(lines) + "\n")

def generate_script(reference_timestamp: str, 
                    recording_datetime: datetime, 
                    input_file: str, 
                    debug: bool) \
                        -> str:

    # Parse the reference timestamp and recording datetime
    reference_seconds = timedelta(hours=int(reference_timestamp.split(":")[0]),
                                  minutes=int(reference_timestamp.split(":")[1]),
                                  seconds=int(reference_timestamp.split(":")[2])).total_seconds()
    recording_datetime = datetime.strptime(recording_datetime, "%Y-%m-%d %H:%M:%S")

    # Read the segment data from the input file
    data = []
    if debug:
        print(f"Opening csv file {input_file}")
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  # Assuming the CSV is comma-separated
        i = 0
        for row in reader:
            i += 1
            if i == 1: # Skip title row
                continue
            # Check if row has at least the expected number of elements
            if len(row) >= 5:
                # Expecting each row as: date, time, artist, start, end
                data.append((row[0], row[1], row[2], row[3], row[4] if len(row) >= 5 else None))
            else:
                if debug:
                    print(f"Skipping malformed row: {row}")

    # Function to convert time strings to seconds
    def time_to_seconds(time_str: str):
        h, m, s = 0, 0, 0
        parts = time_str.split(":")
        if len(parts) == 3:
            h, m, s = map(int, parts)
        elif len(parts) == 2:
            m, s = map(int, parts)
        elif len(parts) == 1:
            s = int(parts[0])
        return timedelta(hours=h, minutes=m, seconds=s).total_seconds()

    # Function to convert seconds to a human-readable time format based on a custom reference
    def seconds_to_human_time(seconds, reference_seconds, recording_datetime):
        adjusted_time = recording_datetime + timedelta(seconds=(seconds - reference_seconds))
        return adjusted_time.strftime("%Y-%m-%d_%H%M")

    # Prepare the bash script content
    script_lines = [
        "#!/bin/bash\n",
        "# Input audio file (replace with your file path)",
        'input_file="$1"\n\n',
        'if [ -z "$1" ]; then\n  echo "Usage: $0 <input_audio_file>"\n  exit 1\nfi\n'
    ]

    # Create ffmpeg commands for each audio segment
    for date, time, artist, start, end in data:
        start_seconds = int(time_to_seconds(start))
        end_seconds = int(time_to_seconds(end)) if end else None

        # Generate human-readable begin time for filename
        human_start_time = seconds_to_human_time(start_seconds, reference_seconds, recording_datetime)

        # Format artist name for filename
        artist_formatted = artist.replace(" ", "-").replace("+", "plus").replace("/", "-")
        
        # Generate output filename
        output_file = f"{human_start_time}_{artist_formatted}.mp3"
        
        # Create ffmpeg command
        if end_seconds is not None:
            command = f'ffmpeg -i "$input_file" -ss {start_seconds} -to {end_seconds} -c:a copy "{output_file}"'
        else:
            command = f'ffmpeg -i "$input_file" -ss {start_seconds} -c:a copy "{output_file}"'
        
        # Add command to script
        script_lines.append(command)

    # Final message
    script_lines.append('\necho "Splitting completed!"')

    # Join and print the script lines as the output
    final_script = "\n".join(script_lines)
    print(final_script)

    return final_script

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a bash script to split audio based on segments and reference time.")
    parser.add_argument("reference_timestamp", type=str, help="Reference timestamp in HH:MM:SS format (e.g., 01:26:31).")
    parser.add_argument("recording_datetime", type=str, help="Datetime that represents the given moment of time of the recording in YYYY-MM-DD HH:MM:SS format.")
    parser.add_argument("--input-file", type=str, required=True, help="Path to the CSV file with audio segment data.")
    parser.add_argument("-o", "--output-file", type=str, help="Output file to save the script", default=None)
    parser.add_argument(
        '--debug',
        action='store_true', 
        help='print debug messages to stderr'
    )
    args = parser.parse_args()
    
    script = generate_script(args.reference_timestamp, args.recording_datetime, args.input_file, args.debug)
    if args.output_file is not None:
        print("Saving to file: {args.output_file}")
        save_to_file(script, args.output_file)
    

