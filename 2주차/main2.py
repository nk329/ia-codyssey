# Mars_Base_Inventory_List.csv 처리 코드

def read_csv(file_path):
    """CSV 파일을 읽고 내용을 리스트(List) 객체로 변환"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 모든 줄 읽기
            inventory = []

            for line in lines[1:]:  # 첫 번째 줄(헤더) 제외
                name, flammability = line.strip().split(',')
                inventory.append((name, float(flammability)))  # 튜플 형태로 저장
            
            return inventory
    
    except FileNotFoundError:
        print(f'❌ 오류: "{file_path}" 파일을 찾을 수 없습니다.')
        return []
    except Exception as e:
        print(f'❌ 예기치 않은 오류 발생: {e}')
        return []

def sort_by_flammability(inventory):
    """인화성이 높은 순으로 정렬"""
    return sorted(inventory, key=lambda x: x[1], reverse=True)

def filter_dangerous_materials(inventory, threshold=0.7):
    """인화성 지수가 특정 값(threshold) 이상인 위험한 물질 필터링"""
    return [item for item in inventory if item[1] >= threshold]

def save_to_csv(file_path, data):
    """리스트 데이터를 CSV 파일로 저장"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('Name,Flammability\n')  # 헤더 작성
            for item in data:
                file.write(f'{item[0]},{item[1]}\n')
        print(f'✅ 위험한 물질 목록이 "{file_path}"에 저장되었습니다.')
    except Exception as e:
        print(f'❌ CSV 파일 저장 중 오류 발생: {e}')

# 파일 경로
csv_file_path = '/mnt/data/Mars_Base_Inventory_List.csv'
dangerous_csv_path = '/mnt/data/Mars_Base_Inventory_danger.csv'

# CSV 파일 읽기 및 처리
inventory_list = read_csv(csv_file_path)

# 인화성이 높은 순으로 정렬
sorted_inventory = sort_by_flammability(inventory_list)

# 인화성 지수가 0.7 이상인 위험한 물질 필터링
dangerous_materials = filter_dangerous_materials(sorted_inventory)

# 결과 출력
print("🔥 인화성이 높은 순으로 정렬된 화물 목록:")
for item in sorted_inventory:
    print(f"{item[0]} - 인화성 지수: {item[1]}")

print("\n🚨 위험한 인화성 물질 (0.7 이상):")
for item in dangerous_materials:
    print(f"{item[0]} - 인화성 지수: {item[1]}")

# 위험한 물질을 새로운 CSV 파일로 저장
save_to_csv(dangerous_csv_path, dangerous_materials)
