import random
import datetime

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
    
    def get_env(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
