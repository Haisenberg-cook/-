import streamlit as st
import matplotlib.pyplot as plt
import csv
# Імпортуємо наші класи з файлу models.py
from models import School, SchoolClass, Student

# --- Функції для обробки даних ---

def load_school_data(csv_path: str) -> School:
    """
    Зчитує CSV файл і перетворює рядки тексту на об'єкти класів.
    """
    school = School("Школа №1")
    
    # Допоміжний словник, щоб швидко знаходити об'єкт класу за назвою ")
    # Це дозволяє не створювати дублікати класів.
    classes_map = {}

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = int(row['parallel'])
                v = row['vertical']
                class_key = f"{p}-{v}"

                # Якщо такого класу ще немає в пам'яті - створюємо його
                if class_key not in classes_map:
                    new_class = SchoolClass(p, v)
                    classes_map[class_key] = new_class
                    school.add_class(new_class)

                # Створюємо об'єкт учня з даних рядка
                student = Student(
                    surname=row['surname'],
                    name=row['name'],
                    patronymic=row['patronymic'],
                    birth_year=int(row['birth_year']),
                    gender=row['gender'],
                    average_grade=float(row['avg_grade'])
                )
                # Додаємо учня у відповідний клас
                classes_map[class_key].add_student(student)
    except FileNotFoundError:
        st.error("Файл students.csv не знайдено! Спочатку запустіть data_generator.py")
        return None

    return school

def show_statistics(school: School):
    """Виводить текстову статистику на екран."""
    # List comprehension: розгортаємо всіх учнів з усіх класів в один список
    all_students = [s for c in school.classes for s in c.students]
    total_students = len(all_students)
    
    if total_students == 0:
        st.warning("У школі немає учнів.")
        return

    # Метрики Streamlit
    st.metric("Загальна кількість учнів", total_students)

    # Підрахунок хлопців
    boys = sum(1 for s in all_students if s.gender == 'Male')
    girls = total_students - boys
    
    col1, col2 = st.columns(2)
    col1.metric("Хлопці", f"{boys} ({boys/total_students:.1%})")
    col2.metric("Дівчата", f"{girls} ({girls/total_students:.1%})")

    # Пошук найбільшого та найменшого класу
    if school.classes:
        max_class = max(school.classes, key=lambda c: len(c.students))
        min_class = min(school.classes, key=lambda c: len(c.students))
        st.write(f"**Найбільший клас:** {max_class.name} ({len(max_class.students)} учнів)")
        st.write(f"**Найменший клас:** {min_class.name} ({len(min_class.students)} учнів)")

def show_charts(school: School):
    """Будує графіки за допомогою Matplotlib."""
    # a. Графік розподілу по паралелях
    parallels = sorted(list(set(c.parallel for c in school.classes)))
    # Рахуємо скільки учнів на кожній паралелі
    counts = [sum(len(c.students) for c in school.classes if c.parallel == p) for p in parallels]
    
    fig1, ax1 = plt.subplots()
    ax1.bar(parallels, counts, color='skyblue')
    ax1.set_title("Учнів по паралелях")
    ax1.set_xlabel("Паралель")
    ax1.set_ylabel("Кількість")
    st.pyplot(fig1)

    # d. Scatter plot (Точкова діаграма)
    x_vals = [] # Номер класу
    y_vals = [] # Середня оцінка
    for c in school.classes:
        for s in c.students:
            x_vals.append(c.parallel)
            y_vals.append(s.average_grade)
            
    fig4, ax4 = plt.subplots()
    ax4.scatter(x_vals, y_vals, alpha=0.5, color='green')
    ax4.set_title("Залежність оцінки від класу")
    ax4.set_xlabel("Клас")
    ax4.set_ylabel("Середня оцінка")
    st.pyplot(fig4)


# --- ГОЛОВНА ЧАСТИНА ПРОГРАМИ ---

st.title(" Аналіз Школи (Сценарій 1)")

# Використовуємо st.session_state, щоб об'єкт школи зберігався в пам'яті
# між натисканнями кнопок (перезавантаженнями сторінки).
if 'school' not in st.session_state:
    st.session_state.school = load_school_data('students.csv')

school = st.session_state.school

if school:
    st.header("Поточний стан")
    show_statistics(school)
    
    with st.expander("Переглянути графіки"):
        show_charts(school)

    st.markdown("---")
    # Кнопка для переведення року
    if st.button("🚀 Перевести школу на наступний рік"):
        new_classes = []
        graduated_count = 0
        
        for c in school.classes:
            # Метод promote() повертає True, якщо клас перейшов далі,
            # і False, якщо це був 11 клас (випуск).
            if c.promote():
                new_classes.append(c)
            else:
                graduated_count += len(c.students)
        
        # Оновлюємо список класів у школі
        school.classes = new_classes
        # Зберігаємо оновлений стан
        st.session_state.school = school 
        
        st.success(f"Навчальний рік завершено! Випустилося {graduated_count} учнів.")
        # Перезавантажуємо сторінку, щоб оновити статистику
        st.rerun()