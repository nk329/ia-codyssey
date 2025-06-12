import csv
import mysql.connector
from datetime import datetime


class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_weather(self, mars_date, temp, storm):
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        self.cursor.execute(query, (mars_date, temp, storm))

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

def read_and_insert_csv(file_path, db_helper):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        print('📌 CSV 헤더:', header)

        for index, row in enumerate(reader, start=2):
            if len(row) < 4:
                print(f'⚠️ {index}번째 줄: 컬럼 수 부족 → {row}')
                continue
            try:
                mars_date = datetime.strptime(row[1], '%Y-%m-%d')  # ✅ 포맷 변경
                temp = float(row[2])  # CSV에 소수점 있는 값도 있으므로 float
                storm = int(row[3])
                db_helper.insert_weather(mars_date, int(temp), storm)
            except ValueError as e:
                print(f'❌ {index}번째 줄: 형식 오류 → {e} → {row}')
            except Exception as e:
                print(f'🔥 {index}번째 줄: 예외 발생 → {e} → {row}')
    db_helper.commit()




def main():
    db = MySQLHelper('localhost', 'root', '1234', 'mars_mission')
    read_and_insert_csv('mars_weathers_data.csv', db)
    db.close()


if __name__ == '__main__':
    main()
