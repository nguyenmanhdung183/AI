import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import re
import yt_dlp
import os

file_path = "socute.csv"
column_index = 2

def is_youtube_link(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, value)


def download_youtube_video(link, column1_value, column2_value):
    try:
        ydl_opts = {
            'outtmpl': os.path.join('videos', f'{column1_value}.%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',  # Ensure the output is in mp4 format
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            print(f"Downloaded YouTube video: {column1_value}-{column2_value}")
    except Exception as e:
        print(f"Error downloading YouTube video {column1_value}-{column2_value}: {e}")
        
def download_video(link, id):
    cookies = {
        '_ga': 'GA1.1.1017532922.1708538541',
        '_ga_ZSF3D6YSLC': 'GS1.1.1708538540.1.1.1708538753.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/vi',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/vi',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'vi',
        'tt': 'aXhmUGVj',
    }

    retry_time = 0
    total_retry_time = 0

    while total_retry_time < 20:
        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

        download_soup = BeautifulSoup(response.text, "html.parser")
        download_link_tag = download_soup.find('a', {'href': True})

        if download_link_tag:
            download_link = download_link_tag['href']

            if download_link.startswith('/vi'):
                download_link = 'https://ssstik.io' + download_link

            video_title_tag = download_soup.find('p')
            video_title = video_title_tag.get_text().strip()

            valid_filename = re.sub(r'[\/:*?"<>|]', '', f"{id}-{video_title}.mp4")

            print(f"STEP 5: Saving the video {id} :)")
            try:
                mp4_file = urlopen(download_link)

                with open(f"videos/{valid_filename}", "wb") as output:
                    while True:
                        data = mp4_file.read(4096)
                        if data:
                            output.write(data)
                        else:
                            break
                break  # Đã tải thành công, thoát khỏi vòng lặp retry
            except Exception as e:
                print(f"Error downloading video {id}: {e}")
        else:
            print(f"Error: Unable to find download link for video {id}")
            retry_time = 1  # Thời gian chờ giữa các lần retry
            total_retry_time += retry_time
            print(f"Retrying in {retry_time} seconds...")
            time.sleep(retry_time)

# Đọc dữ liệu từ file và tải video
# Đọc dữ liệu từ file và tải video
with open(file_path, mode="r", encoding="utf-8-sig") as file:
    # Bỏ qua hàng đầu tiên
    file.readline()
    
    while True:
        line = file.readline().strip()
        if not line:
            break

        data = line.split(',')
        if len(data) >= 2:
            column1_value = data[0].strip()
            column2_value = data[1].strip()
            link_value = data[1].strip()

            # Kiểm tra nếu cột 1 không rỗng
            if column2_value:
                if is_youtube_link(link_value):
                    download_youtube_video(link_value, column1_value, column2_value)
                else:
                    download_video(link_value, column1_value)
                time.sleep(2)  # Thời gian chờ giữa các dòng trong file
            else:
                print(f"Skipping empty value in column 1 for {column1_value}")
