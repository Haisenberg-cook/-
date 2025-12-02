import csv
import random

# Налаштування для генерації
parallels = range(1, 12) # Класи від 1 до 11
verticals = ['А', 'Б']   # Букви класів
students_count = 200     # Загальна кількість учнів

# Списки імен для випадкового вибору
first_names_m = ["Олександр", "Максим", "Дмитро", "Артем", "Іван"]
first_names_f = ["Анна", "Софія", "Марія", "Вікторія", "Дарина"]
surnames = ["Коваленко", "Бондаренко", "Ткаченко", "Шевченко", "Кравченко"]
patronymics = ["Олександрович", "Іванович", "Дмитрович"]

data = []

print("Генерація даних...")

for _ in range(students_count):
    # Випадково обираємо стать
    gender = random.choice(['Male', 'Female'])
    
    # Формуємо ПІБ залежно від статі
    if gender == 'Male':
        name = random.choice(first_names_m)
        patronymic = random.choice(patronymics)
    else:
        name = random.choice(first_names_f)
        # Робимо жіноче по батькові (Олександрович -> Олександрівна) - спрощено
        patronymic = random.choice(patronymics).replace("вич", "вна")
    
    surname = random.choice(surnames)
    
    # Обираємо клас
    parallel = random.choice(parallels)
    vertical = random.choice(verticals)
    
    # Логіка для року народження: чим старший клас, тим раніше народився учень.
    # 2017 - це приблизний рік народження першокласників.
    birth_year = 2017 - parallel + random.randint(-1, 1)
    
    # Випадкова середня оцінка (від 5.0 до 12.0)
    avg_grade = round(random.uniform(5.0, 12.0), 1)

    # Додаємо запис у список
    data.append([surname, name, patronymic, birth_year, gender, avg_grade, parallel, vertical])

# Запис у CSV файл
# newline='' потрібен, щоб не було пустих рядків між даними у Windows
with open('students.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    # Записуємо заголовок (header)
    writer.writerow(['surname', 'name', 'patronymic', 'birth_year', 'gender', 'avg_grade', 'parallel', 'vertical'])
    # Записуємо дані
    writer.writerows(data)

print("Файл students.csv успішно створено! Можна запускати Сценарій 1.")