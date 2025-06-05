import os
import csv
import speech_recognition as sr

def get_audio_files(directory):
    audio_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.wav') or file_name.endswith('.mp3'):
            audio_files.append(file_name)
    return audio_files

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = '인식 실패'
    except sr.RequestError:
        text = 'STT 서비스 에러'
    return text

def save_transcription_to_csv(audio_file_name, transcription_text):
    csv_file_name = audio_file_name.rsplit('.', 1)[0] + '.csv'
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['시간', '인식된 텍스트'])
        writer.writerow(['전체', transcription_text])

def search_keyword_in_csv(directory, keyword):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if keyword in ','.join(row):
                        print(f'{file_name}: {row}')

def main():
    audio_dir = '.'  # 현재 디렉토리
    audio_files = get_audio_files(audio_dir)

    for audio_file in audio_files:
        print(f'처리 중: {audio_file}')
        transcription = transcribe_audio(audio_file)
        save_transcription_to_csv(audio_file, transcription)

    # 보너스 기능 예시 실행
    keyword = input('검색할 키워드를 입력하세요: ')
    search_keyword_in_csv(audio_dir, keyword)

if __name__ == '__main__':
    main()
