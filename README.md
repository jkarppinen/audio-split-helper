
# Audio Split Helper

A Python script that generates a Bash script for splitting an audio file into segments based on specified timestamps and artist information. This is useful for creating separate audio files from a single recording, such as an full event recording with multiple performers during the timespan.

## Features
- Reads audio segment data from a CSV file.
- Uses a reference timestamp and recording start datetime to accurately label each segment.
- Outputs a Bash script with `ffmpeg` commands to split the audio file based on the specified segments.
- Includes a debug mode for detailed console output during execution.

## Requirements
- Python 3.6 or higher
- `ffmpeg` installed and accessible from the command line
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/jkarppinen/audio-split-helper.git
cd audio-split-helper
```

### Installing Dependencies

This project uses Poetry for dependency management.

## Usage

The script reads from a CSV file with the following structure (comma-separated columns):

```plaintext
Date,Time,Artist,Start,End
2024-10-25,22:30,MZA b2b Korai,0:00,1:26:31
2024-10-26,00:00,Histec,1:26:31,2:25:00
...
```

- **Date**: The date of the segment.
- **Time**: The starting time of the segment in the recording.
- **Artist**: The artist or track name.
- **Start**: The segment start time within the recording.
- **End**: The segment end time within the recording (optional for the last segment).

### Running the Script with Poetry

To run the script using Poetry, use the following command format:

```bash
poetry run python audio_split_helper.py <reference_timestamp> <recording_datetime> --input-file <path_to_csv> [--debug]
```

#### Positional Arguments

- `<reference_timestamp>`: Reference timestamp in `HH:MM:SS` format, indicating the specific timestamp within the recording to treat as 00:00:00 (e.g., `01:26:31`).
- `<recording_datetime>`: Actual datetime representing the real-world time of the recording’s start, in `YYYY-MM-DD HH:MM:SS` format.

#### Optional Arguments

- `--input-file`: Path to the CSV file with the audio segment data.
- `--debug`: Enables debug mode, which outputs additional information to the console.

### Example

Assuming you have a CSV file named `segments.csv`, you can generate the script as follows:

```bash
poetry run python audio_split_helper.py 01:26:31 "2024-10-26 00:00:00" --input-file segments.csv --debug
```

This will output a Bash script with `ffmpeg` commands to split the audio based on the specified segments.

## Debug Mode

Use the `--debug` flag to get detailed output, which is helpful for troubleshooting issues with CSV reading or timestamp calculations. The debug messages will indicate:
- When the CSV file is opened.
- Information about each row processed.
- Notifications for any malformed rows skipped.

## Output

The script outputs a Bash script that you can save and run to split the audio file. Each segment is labeled with the calculated timestamp and artist name, in a format like:

```bash
ffmpeg -i "$input_file" -ss <start_time_in_seconds> -to <end_time_in_seconds> -c:a copy "<output_file>.mp3"
```

Example output filenames:

```plaintext
2024-10-25_2230_MZA-b2b-Korai.mp3
2024-10-26_0000_Histec.mp3
```

## Tests

To run all tests, use:

```sh
poetry run pytest
```

To run tests **with coverage**:

```sh
poetry run pytest --cov=script  # Replace 'script' with your module name
```

To run a **specific test file**:

```sh
poetry run pytest tests/test_script.py
```

To run a **single test function**:

```sh
poetry run pytest tests/test_script.py::test_generate_script_valid
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

