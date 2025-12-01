import zipfile
import time
import string
import itertools
import os

def unlock_zip():
    zip_filename = 'emergency_storage_key.zip'
    output_password_file = 'password.txt'
    charset = string.ascii_lowercase + string.digits
    max_length = 6

    try:
        zip_file = zipfile.ZipFile(zip_filename)
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {zip_filename}')
        return
    except zipfile.BadZipFile:
        print(f'잘못된 ZIP 파일입니다: {zip_filename}')
        return

    print('비밀번호 크래킹을 시작합니다...')
    start_time = time.time()
    attempt = 0

    for password_tuple in itertools.product(charset, repeat=max_length):
        password = ''.join(password_tuple)
        attempt += 1

        try:
            zip_file.extractall(pwd=bytes(password, 'utf-8'))
            # 확인용 파일 하나 존재하는지 검사
            test_files = zip_file.namelist()
            if not test_files:
                continue
            with open(output_password_file, 'w') as f:
                f.write(password)
            elapsed_time = time.time() - start_time
            print(f'[성공] 비밀번호: {password}')
            print(f'총 시도 횟수: {attempt}')
            print(f'총 소요 시간: {elapsed_time:.2f}초')
            return
        except (RuntimeError, zipfile.BadZipFile, OSError, Exception):
            continue

    print('비밀번호를 찾지 못했습니다.')

if __name__ == '__main__':
    unlock_zip()
