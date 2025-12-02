import csv
from models import Director, Teacher, SecurityGuard

def main():
    print("--- Сценарій 2: Розрахунок зарплат працівників ---")

    # Створюємо список різних об'єктів.
    # Завдяки ПОЛІМОРФІЗМУ ми можемо зберігати їх в одному списку
    # і обробляти однаково, хоча це різні класи.
    employees = [
        Director("Петренко Василь Іванович", base_salary=15000, pedagogical_experience=20, management_experience=5),
        Teacher("Іваненко Марія Петрівна", base_salary=12000, pedagogical_experience=10),
        Teacher("Сидоренко Олег Олегович", base_salary=12000, pedagogical_experience=2),
        SecurityGuard("Коваленко Петро", base_salary=11000, work_experience=5)
    ]

    output_file = "salaries.csv"
    
    # Відкриваємо файл для запису результатів
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ПІБ", "Посада", "Зарплата"])
        
        print(f"{'Посада':<15} | {'ПІБ':<25} | {'Зарплата'}")
        print("-" * 55)

        for emp in employees:
            # Тут спрацьовує ПОЛІМОРФІЗМ:
            # Ми викликаємо .calculate_salary() для кожного працівника.
            # Python сам знає, чий саме метод викликати (директора, вчителя чи охоронця),
            # тому формула розрахунку буде різною для кожного.
            salary = emp.calculate_salary()
            
            # type(emp).__name__ повертає назву класу (напр., 'Director')
            position = type(emp).__name__ 
            
            print(f"{position:<15} | {emp.full_name:<25} | {salary:.2f} грн")
            
            # Записуємо рядок у файл
            writer.writerow([emp.full_name, position, round(salary, 2)])

    print(f"\nРозрахунок завершено. Таблицю збережено у файл '{output_file}'")

if __name__ == "__main__":
    main()