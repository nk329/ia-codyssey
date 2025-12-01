print("Hello Mars")

def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f'Error: The file "{file_path}" was not found.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    log_file_path = 'mission_computer_main.log'
    read_log_file(log_file_path)
