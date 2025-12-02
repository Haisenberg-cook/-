import csv
from models import Director, Teacher, SecurityGuard

def main():
    print("--- Сценарій 2: Розрахунок зарплат ---")

    # 1. Створення працівників
    employees = [
        Director("Петренко Василь Іванович", base_salary=15000, pedagogical_experience=20, management_experience=5),
        Teacher("Іваненко Марія Петрівна", base_salary=12000, pedagogical_experience=10),
        Teacher("Сидоренко Олег Олегович", base_salary=12000, pedagogical_experience=2),
        SecurityGuard("Коваленко Петро", base_salary=11000, work_experience=5)
    ]

    # 2. Розрахунок та збереження
    output_file = "salaries.csv"
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ПІБ", "Посада", "Зарплата"])
        
        for emp in employees:
            salary = emp.calculate_salary()
            # Визначаємо посаду за класом
            position = type(emp).__name__ 
            
            print(f"{position:<15} | {emp.full_name:<25} | {salary:.2f} грн")
            writer.writerow([emp.full_name, position, round(salary, 2)])

    print(f"\nДані збережено у файл {output_file}")

if __name__ == "__main__":
    main()