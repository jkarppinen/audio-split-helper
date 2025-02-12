# Note: Appending parent folder to make imports work correctly
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tempfile
from datetime import datetime
from audio_split_helper import generate_script, save_to_file  # Adjust import as needed
from io import StringIO
from unittest.mock import patch

class TestScriptGeneration(unittest.TestCase):

    def setUp(self):
        """Set up test data"""
        self.reference_timestamp = "01:26:31"
        self.recording_datetime = "2025-02-12 15:30:00"
        self.valid_csv_content = """date,time,artist,start,end
        2025-02-12,15:30,Artist A,00:05:00,00:10:00
        2025-02-12,15:40,Artist B,00:15:00,
        """
        self.invalid_csv_content = """date,time,artist,start
        2025-02-12,15:30,Artist A,00:05:00
        """

    def test_generate_script_valid(self):
        """Test script generation with a valid CSV file"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_csv:
            temp_csv.write(self.valid_csv_content)
            temp_csv.close()
            script = generate_script(self.reference_timestamp, self.recording_datetime, temp_csv.name, False)
            self.assertIn("ffmpeg -i", script)
            self.assertIn("Artist-A.mp3", script)
        os.remove(temp_csv.name)

    def test_generate_script_invalid_csv(self):
        """Test handling of invalid CSV (missing columns)"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_csv:
            temp_csv.write(self.invalid_csv_content)
            temp_csv.close()
            script = generate_script(self.reference_timestamp, self.recording_datetime, temp_csv.name, False)
            self.assertNotIn("ffmpeg -i", script)  # Should not contain commands
        os.remove(temp_csv.name)

    def test_generate_script_debug_mode(self):
        """Test debug mode output by capturing printed messages"""
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_csv:
            temp_csv.write(self.valid_csv_content)
            temp_csv.close()
            
            with patch("sys.stdout", new=StringIO()) as fake_out:
                generate_script(self.reference_timestamp, self.recording_datetime, temp_csv.name, True)
                output = fake_out.getvalue()
            
            self.assertIn("Opening csv file", output)  # Debug should print file opening message
            
        os.remove(temp_csv.name)

    def test_generate_script_invalid_timestamp(self):
        """Test handling of incorrect timestamp format"""
        with self.assertRaises(ValueError):
            generate_script("invalid:timestamp", self.recording_datetime, "dummy.csv", False)

    def test_save_to_file(self):
        """Test saving generated script to file"""
        script_lines = ["#!/bin/bash", "echo 'Hello World'"]
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        save_to_file(script_lines, temp_filename)

        with open(temp_filename, "r") as f:
            content = f.read()

        self.assertIn("#!/bin/bash", content)
        self.assertIn("echo 'Hello World'", content)
        os.remove(temp_filename)

if __name__ == '__main__':
    unittest.main()

