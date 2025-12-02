import csv
import random

# Параметри генерації
parallels = range(1, 12)
verticals = ['А', 'Б']
students_count = 200

first_names_m = ["Олександр", "Максим", "Дмитро", "Артем", "Іван"]
first_names_f = ["Анна", "Софія", "Марія", "Вікторія", "Дарина"]
surnames = ["Коваленко", "Бондаренко", "Ткаченко", "Шевченко", "Кравченко"]
patronymics = ["Олександрович", "Іванович", "Дмитрович"]

data = []

for _ in range(students_count):
    gender = random.choice(['Male', 'Female'])
    if gender == 'Male':
        name = random.choice(first_names_m)
        patronymic = random.choice(patronymics)
    else:
        name = random.choice(first_names_f)
        patronymic = random.choice(patronymics).replace("вич", "вна")
    
    surname = random.choice(surnames)
    
    parallel = random.choice(parallels)
    vertical = random.choice(verticals)
    
    # Рік народження залежить від класу (приблизно)
    birth_year = 2017 - parallel + random.randint(-1, 1)
    avg_grade = round(random.uniform(5.0, 12.0), 1)

    data.append([surname, name, patronymic, birth_year, gender, avg_grade, parallel, vertical])

# Запис у CSV
with open('students.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['surname', 'name', 'patronymic', 'birth_year', 'gender', 'avg_grade', 'parallel', 'vertical'])
    writer.writerows(data)

print("Файл students.csv успішно створено!")