import moviepy.editor as mp
import speech_recognition as sr

def extract_audio_from_video(video_path, audio_path="temp_audio.wav"):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        # Specify the language as 'zh-CN' for Chinese
        text = recognizer.recognize_google(audio, language='zh-CN')
        print("Text from the audio: ", text)

        # Write the text to a file
        with open("text_chinese.txt", "w", encoding='utf-8') as file:
            file.write(text)
            print("Text written to text_chinese.txt")
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Error connecting to the Google Web Speech API: {e}")

if __name__ == "__main__":
    video_path = "video.mp4"  # Replace with your video file path
    audio_path = extract_audio_from_video(video_path)
    convert_audio_to_text(audio_path)
