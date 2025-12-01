import time
import json
import random
import msvcrt


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def random_date(self, start_year, end_year):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28) 
        return f"{year}-{month:02d}-{day:02d}"

    def random_time(self):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}:{second:02d}"
    
    def get_env(self):
        random_generated_date = self.random_date(2020, 2025)  
        random_generated_time = self.random_time()  
        current_time = f"{random_generated_date} {random_generated_time}"
        log_entry = f"{current_time}, {self.env_values['mars_base_internal_temperature']}, " \
                    f"{self.env_values['mars_base_external_temperature']}, {self.env_values['mars_base_internal_humidity']}, " \
                    f"{self.env_values['mars_base_external_illuminance']}, {self.env_values['mars_base_internal_co2']}, " \
                    f"{self.env_values['mars_base_internal_oxygen']}\n"
        
        with open('sensor_log.txt', 'a') as log_file:
            log_file.write(log_entry)
        
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        self.readings = []
        self.start_time = time.time()

    def get_sensor_data(self):
        while True:
            # 보너스: 특정 키('q')가 눌리면 반복 종료
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'q':
                    print('Sytem stoped….')
                    break

            # 센서 데이터를 갱신하고 가져옴
            self.ds.set_env()
            sensor_data = self.ds.get_env()
            self.env_values = sensor_data
            # 센서 데이터를 JSON 형식으로 출력
            print(json.dumps(self.env_values))
            # 현재 값을 별도의 리스트에 저장(5분 평균 계산용)
            self.readings.append(sensor_data.copy())

            # 5분(300초)이 경과했는지 확인하고 평균 계산 후 출력
            current_time = time.time()
            if current_time - self.start_time >= 300:
                count = len(self.readings)
                sums = {key: 0 for key in self.env_values}
                for reading in self.readings:
                    for key, value in reading.items():
                        sums[key] += value
                avg_values = {key: sums[key] / count for key in sums}
                print('5분 평균값:')
                print(json.dumps(avg_values))
                # 5분 평균 출력 후 초기화
                self.start_time = current_time
                self.readings = []

            time.sleep(5)


if __name__ == '__main__':
    # MissionComputer 클래스를 RunComputer라는 이름의 인스턴스로 생성하고,
    # get_sensor_data() 메소드 호출하여 지속적으로 센서 데이터 출력
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
