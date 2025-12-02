import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
from models import School, SchoolClass, Student

# --- Допоміжні функції ---

def load_school_data(csv_path: str) -> School:
    school = School("Школа №1")
    
    # Словник для тимчасового зберігання класів: "1-А" -> SchoolClass
    classes_map = {}

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = int(row['parallel'])
                v = row['vertical']
                class_key = f"{p}-{v}"

                # Створюємо клас, якщо ще немає
                if class_key not in classes_map:
                    new_class = SchoolClass(p, v)
                    classes_map[class_key] = new_class
                    school.add_class(new_class)

                # Створюємо учня
                student = Student(
                    surname=row['surname'],
                    name=row['name'],
                    patronymic=row['patronymic'],
                    birth_year=int(row['birth_year']),
                    gender=row['gender'],
                    average_grade=float(row['avg_grade'])
                )
                classes_map[class_key].add_student(student)
    except FileNotFoundError:
        st.error("Файл students.csv не знайдено! Спочатку запустіть data_generator.py")
        return None

    return school

def show_statistics(school: School):
    # Збираємо всіх учнів в один список для зручності
    all_students = [s for c in school.classes for s in c.students]
    total_students = len(all_students)
    
    if total_students == 0:
        st.warning("У школі немає учнів.")
        return

    # a. Загальна кількість
    st.metric("Загальна кількість учнів", total_students)

    # b. Відсоток хлопців/дівчат
    boys = sum(1 for s in all_students if s.gender == 'Male')
    girls = total_students - boys
    
    col1, col2 = st.columns(2)
    col1.metric("Хлопці", f"{boys} ({boys/total_students:.1%})")
    col2.metric("Дівчата", f"{girls} ({girls/total_students:.1%})")

    # c. Середня кількість у класах
    if school.classes:
        avg_in_class = total_students / len(school.classes)
        st.write(f"**Середня кількість учнів у класі:** {avg_in_class:.1f}")

    # d, e. Max/Min кількість
    if school.classes:
        max_class = max(school.classes, key=lambda c: len(c.students))
        min_class = min(school.classes, key=lambda c: len(c.students))
        st.write(f"**Найбільший клас:** {max_class.name} ({len(max_class.students)} учнів)")
        st.write(f"**Найменший клас:** {min_class.name} ({len(min_class.students)} учнів)")

def show_charts(school: School):
    all_students = [s for c in school.classes for s in c.students]
    
    # a. Розподіл по паралелях
    parallels = sorted(list(set(c.parallel for c in school.classes)))
    counts = [sum(len(c.students) for c in school.classes if c.parallel == p) for p in parallels]
    
    fig1, ax1 = plt.subplots()
    ax1.bar(parallels, counts, color='skyblue')
    ax1.set_title("Учнів по паралелях")
    ax1.set_xticks(parallels)
    st.pyplot(fig1)

    # b. Розподіл по вертикалях
    verticals = sorted(list(set(c.vertical for c in school.classes)))
    avg_counts = []
    for v in verticals:
        classes_v = [c for c in school.classes if c.vertical == v]
        if classes_v:
            avg = sum(len(c.students) for c in classes_v) / len(classes_v)
            avg_counts.append(avg)
        else:
            avg_counts.append(0)
            
    fig2, ax2 = plt.subplots()
    ax2.bar(verticals, avg_counts, color='orange')
    ax2.set_title("Середня кількість учнів по вертикалях")
    st.pyplot(fig2)

    # c. Лінійний графік від року народження
    years = sorted(list(set(s.birth_year for s in all_students)))
    years_counts = [sum(1 for s in all_students if s.birth_year == y) for y in years]
    
    fig3, ax3 = plt.subplots()
    ax3.plot(years, years_counts, marker='o')
    ax3.set_title("Кількість учнів за роком народження")
    st.pyplot(fig3)

    # d. Scatter (Середня оцінка від класу)
    # Перетворимо назви класів в числа для осі X (наприклад, 1-А -> 1.0, 1-Б -> 1.5)
    # Або просто візьмемо паралель
    x_vals = []
    y_vals = []
    for c in school.classes:
        for s in c.students:
            x_vals.append(c.parallel)
            y_vals.append(s.average_grade)
            
    fig4, ax4 = plt.subplots()
    ax4.scatter(x_vals, y_vals, alpha=0.5)
    ax4.set_title("Середня оцінка vs Паралель")
    ax4.set_xlabel("Паралель")
    ax4.set_ylabel("Оцінка")
    st.pyplot(fig4)


# --- Основна логіка ---

st.title(" Аналіз Школи (Сценарій 1)")

if 'school' not in st.session_state:
    st.session_state.school = load_school_data('students.csv')

school = st.session_state.school

if school:
    st.header("Поточний стан")
    show_statistics(school)
    
    with st.expander("Графіки"):
        show_charts(school)

    st.markdown("---")
    if st.button(" Перевести школу на наступний рік"):
        # Логіка переведення
        new_classes = []
        graduated_count = 0
        
        for c in school.classes:
            if c.promote():
                new_classes.append(c)
            else:
                graduated_count += len(c.students)
        
        school.classes = new_classes
        st.session_state.school = school # Оновлюємо стан
        st.success(f"Рік завершено! Випустилося {graduated_count} учнів.")
        st.rerun()