# javis.py

import os
import datetime
import sounddevice as sd
import scipy.io.wavfile as wavfile

RECORD_SECONDS = 5
SAMPLE_RATE = 44100
CHANNELS = 1


def create_records_directory():
    if not os.path.exists('records'):
        os.makedirs('records')


def get_timestamp_filename():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S') + '.wav'


def record_voice():
    print('녹음을 시작합니다. 말하세요...')
    recording = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                       channels=CHANNELS, dtype='int16')
    sd.wait()
    print('녹음이 완료되었습니다.')
    return recording


def save_recording(recording, filename):
    filepath = os.path.join('records', filename)
    wavfile.write(filepath, SAMPLE_RATE, recording)
    print(f'파일이 저장되었습니다: {filepath}')


def list_recordings_in_range(start_date, end_date):
    print(f'[{start_date} ~ {end_date}] 범위의 녹음 파일 목록:')
    found = False

    for file in os.listdir('records'):
        if file.endswith('.wav'):
            date_part = file.split('-')[0]
            try:
                file_date = datetime.datetime.strptime(date_part, '%Y%m%d').date()
                if start_date <= file_date <= end_date:
                    print(file)
                    found = True
            except ValueError:
                continue

    if not found:
        print('해당 범위에 녹음 파일이 없습니다.')


def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        print('날짜 형식이 잘못되었습니다. 예: 20250529')
        return None


def main():
    create_records_directory()

    print('\n메뉴:')
    print('1. 음성 녹음하기')
    print('2. 날짜 범위의 녹음 파일 조회하기')
    choice = input('선택하세요 (1 또는 2): ')

    if choice == '1':
        filename = get_timestamp_filename()
        recording = record_voice()
        save_recording(recording, filename)

    elif choice == '2':
        start_input = input('시작 날짜를 입력하세요 (예: 20250528): ')
        end_input = input('끝 날짜를 입력하세요 (예: 20250529): ')

        start_date = parse_date(start_input)
        end_date = parse_date(end_input)

        if start_date and end_date:
            list_recordings_in_range(start_date, end_date)

    else:
        print('올바르지 않은 선택입니다.')


if __name__ == '__main__':
    main()
