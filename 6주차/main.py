# main.py

def read_log_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            print('[전체 로그 출력 - 최신 순]\n')
            for line in reversed(lines):
                print(line.strip())

            save_error_logs(lines)

    except FileNotFoundError:
        print('로그 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'알 수 없는 오류 발생: {e}')


def save_error_logs(lines):
    error_lines = []
    for line in lines:
        if '[ERROR]' in line:
            error_lines.append(line)

    if error_lines:
        try:
            with open('error_logs.txt', 'w', encoding='utf-8') as error_file:
                for err in error_lines:
                    error_file.write(err)
            print('\n[ERROR 로그가 error_logs.txt 파일로 저장되었습니다.]')
        except Exception as e:
            print(f'오류 로그 저장 중 문제가 발생했습니다: {e}')
    else:
        print('\n[ERROR 로그가 발견되지 않았습니다.]')


if __name__ == '__main__':
    read_log_file('mission_computer_main.log')
