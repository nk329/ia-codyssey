def caesar_cipher_decode(target_text):
    decoded_candidates = []

    for shift in range(1, 26):
        decoded = ''

        for char in target_text:
            if 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded += char

        print(f'[{shift}] {decoded}')
        decoded_candidates.append((shift, decoded))

    return decoded_candidates


def read_password_file():
    try:
        with open('password.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print('[에러] password.txt 파일을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'[에러] 파일 읽기 실패: {e}')
        return None


def write_result_file(decoded_text):
    try:
        with open('result.txt', 'w') as file:
            file.write(decoded_text)
        print('[✔] result.txt 파일에 저장 완료.')
    except Exception as e:
        print(f'[에러] 파일 저장 실패: {e}')


def auto_detect_with_dictionary(decoded_candidates):
    # 아주 간단한 단어 사전
    dictionary = ['mars', 'password', 'hello', 'base', 'station', 'emergency', 'access']

    for shift, decoded in decoded_candidates:
        lower_text = decoded.lower()
        for word in dictionary:
            if word in lower_text:
                print(f'[!] 사전 단어 "{word}" 발견 → 자동 종료 (자리수 {shift})')
                return shift, decoded
    return None, None


def main():
    encrypted_text = read_password_file()
    if encrypted_text is None:
        return

    print('🔓 카이사르 암호 해독 시작...\n')
    candidates = caesar_cipher_decode(encrypted_text)

    # 보너스: 사전 기반 자동 검출
    shift, auto_decoded = auto_detect_with_dictionary(candidates)
    if auto_decoded:
        write_result_file(auto_decoded)
        return

    print('\n👀 위의 결과 중 올바르게 해독된 번호를 입력하세요.')
    try:
        user_choice = int(input('번호 입력 (1~25): '))
        if 1 <= user_choice <= 25:
            _, selected_text = candidates[user_choice - 1]
            write_result_file(selected_text)
        else:
            print('[오류] 유효한 번호가 아닙니다.')
    except Exception:
        print('[오류] 숫자를 정확히 입력하세요.')

if __name__ == '__main__':
    main()
