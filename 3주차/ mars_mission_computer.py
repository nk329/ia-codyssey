import random

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

    def __random_date(start_year, end_year):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # 단순화를 위해 28일로 제한 (2월을 포함한 모든 월을 처리)
        return f"{year}-{month:02d}-{day:02d}"

    def __random_time():
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

# 인스턴스 생성 및 테스트
ds = DummySensor()
ds.set_env()
env_data = ds.get_env()
print(env_data)
