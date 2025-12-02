from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# --- БЛОК 1: Сутності учнів та класів ---

# Використовуємо @dataclass, щоб автоматично створити конструктор (__init__)
# та методи порівняння. Це спрощує код.
@dataclass
class Student:
    """Клас, що представляє сутність Учня."""
    surname: str
    name: str
    patronymic: str
    birth_year: int
    gender: str  # 'Male' або 'Female'
    average_grade: float

    # @property дозволяє звертатися до методу як до змінної (student.full_name)
    # Це приклад інкапсуляції логіки формування імені.
    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"

class SchoolClass:
    """Клас для шкільного класу (наприклад, 9-А)."""
    def __init__(self, parallel: int, vertical: str):
        self.parallel = parallel  # Номер паралелі (1-11)
        self.vertical = vertical  # Літера (А, Б...)
        self.students: List[Student] = [] # Список об'єктів Student (Композиція)

    def add_student(self, student: Student):
        """Додає учня до списку класу."""
        self.students.append(student)

    @property
    def name(self) -> str:
        """Повертає повну назву класу, напр. '5-Б'."""
        return f"{self.parallel}-{self.vertical}"

    def promote(self) -> bool:
        """
        Переводить клас на наступний рік.
        Змінює внутрішній стан об'єкта (номер паралелі).
        Повертає False, якщо клас вже 11-й (випускний).
        """
        if self.parallel >= 11:
            return False  # Клас випускається, далі нікуди
        self.parallel += 1
        return True

# --- БЛОК 2: Сутності працівників (Демонстрація Поліморфізму) ---

# ABC (Abstract Base Class) означає, що ми не можемо створити просто "Працівника".
# Ми мусимо створити конкретний тип (Вчитель, Директор тощо).
class Employee(ABC):
    def __init__(self, full_name: str, base_salary: float):
        self.full_name = full_name
        self.base_salary = base_salary

    # @abstractmethod змушує всі дочірні класи реалізувати цей метод.
    # Це гарантує, що у кожного працівника буде метод розрахунку зарплати.
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

# Клас Вчитель успадковує (Inheritance) властивості Employee
class Teacher(Employee):
    def __init__(self, full_name: str, base_salary: float, pedagogical_experience: int):
        # super().__init__ викликає конструктор батьківського класу,
        # щоб ініціалізувати ім'я та базову ставку.
        super().__init__(full_name, base_salary)
        self.pedagogical_experience = pedagogical_experience

    # Реалізація унікальної логіки зарплати для вчителя
    def calculate_salary(self) -> float:
        bonus = (self.base_salary * self.pedagogical_experience) / 30
        return self.base_salary + bonus

# Директор є Вчителем (має пед. стаж), але з додатковими обов'язками.
# Спадкування: Employee -> Teacher -> Director
class Director(Teacher):
    def __init__(self, full_name: str, base_salary: float, pedagogical_experience: int, management_experience: int):
        # Ініціалізуємо частину "Вчителя" через super()
        super().__init__(full_name, base_salary, pedagogical_experience)
        self.management_experience = management_experience

    # Перевизначення методу для директора
    def calculate_salary(self) -> float:
        # Використовуємо формулу з завдання
        part1 = (self.base_salary * self.pedagogical_experience) / 50
        part2 = self.management_experience * 500
        return self.base_salary + part1 + part2

class SecurityGuard(Employee):
    def __init__(self, full_name: str, base_salary: float, work_experience: int):
        super().__init__(full_name, base_salary)
        self.work_experience = work_experience

    def calculate_salary(self) -> float:
        return self.base_salary + (self.work_experience * 250)

# --- БЛОК 3: Головний контейнер ---

class School:
    """Клас, що об'єднує всі сутності."""
    def __init__(self, name: str):
        self.name = name
        # Школа містить списки класів та працівників
        self.classes: List[SchoolClass] = []
        self.employees: List[Employee] = []

    def add_class(self, school_class: SchoolClass):
        self.classes.append(school_class)

    def add_employee(self, employee: Employee):
        self.employees.append(employee)