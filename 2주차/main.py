import os

# CSV 파일 읽기 함수
def read_csv(file_path):
    """CSV 파일을 읽고 내용을 리스트(List) 객체로 변환"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        inventory = []

        for line in lines[1:]:  # 첫 번째 줄(헤더) 제외

            print(line.strip())
            parts = line.strip().split(',')
            """
            if len(parts) != 2:  # 데이터 개수 확인 (이름, 인화성 지수)
                print(f'⚠️ 경고: 잘못된 형식의 데이터 - {line.strip()} (무시됨)')
                continue
            """


            name, substance,weight,gravity,flammability = parts
            try:
                inventory.append([name, substance,weight,gravity,flammability])  # 숫자로 변환
            except ValueError:
                print(f'⚠️ 경고: 인화성 지수가 숫자가 아님 - {flammability} (무시됨)')
        return inventory


    except FileNotFoundError:
        print(f'❌ 오류: "{file_path}" 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'❌ 예기치 않은 오류 발생: {e}')
        return []

# 인화성이 높은 순으로 정렬
def sort_by_flammability(inventory):
    return sorted(inventory, key=lambda x: x[4], reverse=True)

# 위험한 물질 필터링 (인화성 지수 0.7 이상)
def filter_dangerous_materials(inventory, threshold=0.7):
    return [item for item in inventory if float(item[4]) >= threshold]

# CSV 저장 함수
def save_to_csv(file_path, data):
    """리스트 데이터를 CSV 파일로 저장"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('Name,Flammability\n')
            for item in data:
                file.write(f'{item[0]},{item[4]}\n')
        print(f'✅ 위험한 물질 목록이 "{file_path}"에 저장되었습니다.')
    except Exception as e:
        print(f'❌ CSV 파일 저장 중 오류 발생: {e}')

# 이진 파일 저장 함수
def save_to_binary(file_path, data):
    """정렬된 데이터를 이진 파일로 저장"""
    try:
        with open(file_path, 'wb') as file:
            for item in data:
                line = f'{item[0]},{item[1]}\n'
                file.write(line.encode('utf-8'))  # UTF-8 인코딩 후 저장
        print(f'✅ 정렬된 목록이 이진 파일 "{file_path}"에 저장되었습니다.')
    except Exception as e:
        print(f'❌ 이진 파일 저장 중 오류 발생: {e}')

# 이진 파일 읽기 함수
def read_from_binary(file_path):
    """이진 파일에서 데이터 읽어오기"""
    try:
        with open(file_path, 'rb') as file:
            content = file.read().decode('utf-8')
            print(f'📄 [이진 파일 내용] \n{content}')
    except FileNotFoundError:
        print(f'❌ 오류: "{file_path}" 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'❌ 이진 파일 읽기 중 오류 발생: {e}')

# 파일 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_file_path = os.path.join(script_dir, 'Mars_Base_Inventory_List.csv')
dangerous_csv_path = os.path.join(script_dir, 'Mars_Base_Inventory_danger.csv')
binary_file_path = os.path.join(script_dir, 'Mars_Base_Inventory_List.bin')

# CSV 파일 읽기 및 처리
inventory_list = read_csv(csv_file_path)

# 인화성이 높은 순으로 정렬
sorted_inventory = sort_by_flammability(inventory_list)

# 인화성 지수가 0.7 이상인 위험한 물질 필터링
dangerous_materials = filter_dangerous_materials(sorted_inventory)

print("\n🚨 위험한 인화성 물질 (0.7 이상):")
for item in dangerous_materials:
    print(f"{item[0]} - 인화성 지수: {item[1]}")

# 위험한 물질을 새로운 CSV 파일로 저장
save_to_csv(dangerous_csv_path, dangerous_materials)

# 이진 파일로 저장
save_to_binary(binary_file_path, sorted_inventory)

# 이진 파일 읽어 출력
read_from_binary(binary_file_path)
