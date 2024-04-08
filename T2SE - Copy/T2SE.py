import os
from gtts import gTTS
import csv
import elevenlabs
elevenlabs.set_api_key("0e63e4580e8cf47af0a3c74741e5f1b6")

file_path = "output_file.csv"
name_column_index = 0
data_column_index = 4
output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound")
language = "en"

input_file_path = 'socute.csv'
output_file_path = 'output_file.csv'

# Process CSV and generate MP3
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

modified_data = [[cell.replace(',', '.') for cell in row] for row in data]

with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(modified_data)

print("Data has been saved to the output file.")
print("Start speech...")

# Read the modified CSV file and generate MP3 files
with open(output_file_path, mode='r', encoding="utf-8-sig") as file:
    # Skip the header
    file.readline()

    for line in file:
        data = line.strip().split(',')

        if len(data) < data_column_index + 1:
            continue

        if data[data_column_index].strip() and "#ERROR" not in data[data_column_index]:
            name = data[name_column_index].strip()
            raw_text = data[data_column_index].strip()

            raw_text = raw_text.replace(',', '.')
            text = raw_text.replace('"', '')

            if text:
                print(text)

                # Create a filename based on the value in column 0
                filename = f"{name}.mp3"

                # Determine the full path to save the file in the "sound" directory
                file_path = os.path.join(output_directory, filename)

                voice = elevenlabs.Voice(
                    voice_id="EXAVITQu4vr4xnSDxMaL",
                    settings=elevenlabs.VoiceSettings(
                        stability=0.3,  # Lower is more expressive.
                        similarity_boost=0.75
                    )
                )

                # Generate speech
                speech = elevenlabs.generate(
                    text=text,
                    voice=voice,
                    model="eleven_monolingual_v1"
                )

                # Save the speech to the created file path
                elevenlabs.save(speech, file_path)

print("Speech generation complete.")
