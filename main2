print("Hello Mars")

def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 로그를 시간 기준으로 역순 정렬
        sorted_logs = sorted(lines[1:], reverse=True)  # 헤더 제외 후 역순 정렬

        print("=== 로그 (시간 역순) ===")
        for line in sorted_logs:
            print(line.strip())

        # 문제가 되는 로그 필터링 (산소 탱크 관련 로그)
        error_logs = [line for line in sorted_logs if "Oxygen tank" in line]

        if error_logs:
            with open('error_logs.txt', 'w', encoding='utf-8') as error_file:
                error_file.write("timestamp,event,message\n")  # 헤더 추가
                error_file.writelines(error_logs)

            print("\n🚨 문제가 되는 로그가 'error_logs.txt'에 저장되었습니다.")
        else:
            print("\n✅ 문제가 되는 로그가 발견되지 않았습니다.")

    except FileNotFoundError:
        print(f'Error: The file "{file_path}" was not found.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    log_file_path = 'mission_computer_main.log'
    read_log_file(log_file_path)
