from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

# --- Сутності учнів та класів ---

@dataclass
class Student:
    """Клас, що представляє учня."""
    surname: str
    name: str
    patronymic: str
    birth_year: int
    gender: str  # 'Жіночий' або 'Чоловічий'
    average_grade: float

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"

class SchoolClass:
    """Клас, що представляє шкільний клас (наприклад, 9-А)."""
    def __init__(self, parallel: int, vertical: str):
        self.parallel = parallel  # 1-11
        self.vertical = vertical  # А, Б...
        self.students: List[Student] = []

    def add_student(self, student: Student):
        self.students.append(student)

    @property
    def name(self) -> str:
        return f"{self.parallel}-{self.vertical}"

    def promote(self) -> bool:
        """Переводить клас на рік вперед. Повертає False, якщо клас випускається."""
        if self.parallel >= 11:
            return False  # Клас випускається
        self.parallel += 1
        return True

# --- Сутності працівників (Поліморфізм) ---

class Employee(ABC):
    """Абстрактний базовий клас для працівника."""
    def __init__(self, full_name: str, base_salary: float):
        self.full_name = full_name
        self.base_salary = base_salary

    @abstractmethod
    def calculate_salary(self) -> float:
        """Метод розрахунку зарплати, який має бути реалізований у нащадках."""
        pass

class Teacher(Employee):
    def __init__(self, full_name: str, base_salary: float, pedagogical_experience: int):
        super().__init__(full_name, base_salary)
        self.pedagogical_experience = pedagogical_experience

    def calculate_salary(self) -> float:
        # зарплата = базова ставка * педагогічний стаж / 30
        bonus = (self.base_salary * self.pedagogical_experience) / 30
        return self.base_salary + bonus

class Director(Teacher): # Директор теж вчитель (за логікою стажу)
    def __init__(self, full_name: str, base_salary: float, pedagogical_experience: int, management_experience: int):
        super().__init__(full_name, base_salary, pedagogical_experience)
        self.management_experience = management_experience

    def calculate_salary(self) -> float:
        # Директор: зарплата = базова ставка * педагогічний стаж / 50 + стаж керування * 500
        # (Формула з завдання трохи дивна, бо зменшує базу, але роблю точно як в умові)
        part1 = (self.base_salary * self.pedagogical_experience) / 50
        part2 = self.management_experience * 500
        return self.base_salary + part1 + part2

class SecurityGuard(Employee):
    def __init__(self, full_name: str, base_salary: float, work_experience: int):
        super().__init__(full_name, base_salary)
        self.work_experience = work_experience

    def calculate_salary(self) -> float:
        # Охоронець: зарплата = базова ставка + загальний досвід * 250
        return self.base_salary + (self.work_experience * 250)

# --- Головний клас Школи ---

class School:
    """Клас-контейнер для всієї школи."""
    def __init__(self, name: str):
        self.name = name
        self.classes: List[SchoolClass] = []
        self.employees: List[Employee] = []

    def add_class(self, school_class: SchoolClass):
        self.classes.append(school_class)

    def add_employee(self, employee: Employee):
        self.employees.append(employee)