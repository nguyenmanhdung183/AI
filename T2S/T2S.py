import os
from gtts import gTTS
import csv

file_path = "output_file.csv"
name_column_index = 0
data_column_index = 4
output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound")
language = "en"




input_file_path = 'socute.csv'

# Đường dẫn đến file CSV đầu ra
output_file_path = 'output_file.csv'

# Mở file đầu vào
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
    # Đọc dữ liệu từ file CSV
    reader = csv.reader(input_file)
    data = list(reader)

# Thay đổi tất cả các dấu phẩy thành dấu chấm trong dữ liệu
modified_data = [[cell.replace(',', '.') for cell in row] for row in data]

# Mở file đầu ra để ghi dữ liệu đã sửa
with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    # Sử dụng csv.writer để ghi dữ liệu vào file mới
    writer = csv.writer(output_file)
    writer.writerows(modified_data)

print("Quá trình đã hoàn thành. Dữ liệu đã được lưu trong file mới.")
print("start speech.....")



# Replace commas with dots in the fourth column and create a new CSV file
with open(output_file_path, mode='r', encoding="utf-8-sig") as file:
    lines = file.readlines()


# Read the modified CSV file and generate MP3 files
rows_processed = 0
with open(file_path, mode="r", encoding="utf-8-sig") as file:
    # Skip the header
    file.readline()

    for line in file:
        data = line.strip().split(',')

        # Check if the row has enough elements
        if len(data) < data_column_index + 1:
            continue

        # Check if the data in the specified column is not empty and does not contain "#ERROR"
        if data[data_column_index].strip() and "#ERROR" not in data[data_column_index]:
            name = data[name_column_index].strip()
            raw_text = data[data_column_index].strip()

            # Replace commas with dots
            raw_text = raw_text.replace(',', '.')

            # Remove double quotes from the text
            text = raw_text.replace('"', '')

            # Check if the text is not empty before creating the gTTS object
            if text:
                print(text)

                # Create a filename based on the value in column 0
                filename = f"{name}.mp3"

                # Determine the full path to save the file in the "sound" directory
                file_path = os.path.join(output_directory, filename)

                # Save the speech to the created file
                speech = gTTS(text=text, lang=language, slow=False, tld="com")
                speech.save(file_path)

        rows_processed += 1
