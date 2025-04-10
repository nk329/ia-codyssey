import time
import json
import random
import msvcrt
import platform
import os

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
        return f'{year}-{month:02d}-{day:02d}'

    def random_time(self):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f'{hour:02d}:{minute:02d}:{second:02d}'
    
    def get_env(self):
        random_generated_date = self.random_date(2020, 2025)
        random_generated_time = self.random_time()
        current_time = f'{random_generated_date} {random_generated_time}'
        log_entry = f'{current_time}, {self.env_values["mars_base_internal_temperature"]}, ' \
                    f'{self.env_values["mars_base_external_temperature"]}, {self.env_values["mars_base_internal_humidity"]}, ' \
                    f'{self.env_values["mars_base_external_illuminance"]}, {self.env_values["mars_base_internal_co2"]}, ' \
                    f'{self.env_values["mars_base_internal_oxygen"]}\n'
        
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
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'q':
                    print('System stopped...')
                    # q 누르면 시스템 정보 출력
                    self.get_mission_computer_info()
                    self.get_mission_computer_load()
                    break

            self.ds.set_env()
            sensor_data = self.ds.get_env()
            self.env_values = sensor_data
            print(json.dumps(self.env_values))
            self.readings.append(sensor_data.copy())

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
                self.start_time = current_time
                self.readings = []

            time.sleep(5)

    def get_mission_computer_info(self):
        try:
            system_info = {
                'Operating System': platform.system(),
                'Operating System Version': platform.version(),
                'CPU Type': platform.processor(),
                'CPU Cores': os.cpu_count()
            }
            if platform.system() == 'Windows':
                mem_info = os.popen('systeminfo').read()
                for line in mem_info.split('\n'):
                    if 'Total Physical Memory' in line:
                        memory = line.split(':')[1].strip()
                        system_info['Memory'] = memory
                        break
            else:
                mem_info = os.popen('free -h').readlines()
                if len(mem_info) >= 2:
                    memory = mem_info[1].split()[1]
                    system_info['Memory'] = memory
            print('=== Mission Computer Info ===')
            print(json.dumps(system_info, indent=4, ensure_ascii=False))
        except Exception as e:
            print('시스템 정보 조회 중 오류:', str(e))

    def get_mission_computer_load(self):
        try:
            load_info = {}
            if platform.system() == 'Windows':
                cpu_load = os.popen('wmic cpu get loadpercentage').read()
                cpu_load_lines = cpu_load.strip().split('\n')
                if len(cpu_load_lines) >= 2:
                    cpu_usage = cpu_load_lines[1].strip()
                    load_info['CPU Usage (%)'] = cpu_usage
                mem_info = os.popen('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value').read()
                mem_lines = mem_info.strip().split('\n')
                mem_data = {}
                for line in mem_lines:
                    if '=' in line:
                        key, value = line.split('=')
                        mem_data[key.strip()] = int(value.strip())
                total = mem_data.get('TotalVisibleMemorySize', 0)
                free = mem_data.get('FreePhysicalMemory', 0)
                if total > 0:
                    usage = (total - free) / total * 100
                    load_info['Memory Usage (%)'] = round(usage, 2)
            else:
                load_avg = os.getloadavg()
                load_info['CPU Usage (1min avg)'] = load_avg[0]
                mem_info = os.popen('free').readlines()
                if len(mem_info) >= 2:
                    total = int(mem_info[1].split()[1])
                    used = int(mem_info[1].split()[2])
                    usage = used / total * 100
                    load_info['Memory Usage (%)'] = round(usage, 2)
            print('=== Mission Computer Load ===')
            print(json.dumps(load_info, indent=4, ensure_ascii=False))
        except Exception as e:
            print('시스템 부하 조회 중 오류:', str(e))


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
