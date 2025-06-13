# course-retention-analysis
# Анализ Продлений Курсов / Course Retention Analysis Project

## 🇷🇺 Описание проекта

### Цель проекта:
Разработка полного аналитического цикла для оценки продлений курсов онлайн-школы:
1. Извлечение данных из базы SQL.
2. Предобработка и анализ данных на Python.
3. Создание интерактивных дашбордов в Yandex DataLens и Power BI.

### Этапы проекта:
1) SQL-запрос:
Выгрузка данных по курсам, студентам, домашним заданиям.

Использование CTE для повышения читаемости.

Проверка на корректность соединений.

Результат сохранён в формате .csv.

2) Python-обработка:
Проверка на дубликаты, пропуски, типы данных, выбросы.

Выделение "волн" студентов на курсе по дате подключения.

Финальный датасет сохранён в .csv.

Визуализация данных (boxplot, распределение по волнам).

3) Визуализация (Yandex DataLens & Power BI):
Вкладка Продления курсов: анализ ретеншн по курсам.

Вкладка Ученики курсов: таблица с фильтрами по критериям задания.

В Power BI реализована воронка продлений.

Возможность выгрузки списка студентов для дальнейшей обработки.

### Результат:
✔️ Полностью реализован проект.

✔️ Визуализация позволяет решать бизнес-задачи: поиск учеников определённой волны, не продливших определенный месяц конкретного курса; сравнение retention между разными типами курсов; составление списка учеников для дальнейшей работы с ними.

✔️ Все этапы соответствуют реальному рабочему циклу аналитика.

## 🇬🇧 English Description

### Project Goal:
Building a full data analysis pipeline to evaluate student course retention in an online education platform:
1. Data extraction via SQL.
2. Data preprocessing and analysis in Python.
3. Interactive dashboards in Yandex DataLens and Power BI.

### Project Stages:
1) SQL Query:
Extracted student, course, homework data.

Used CTEs for clarity.

Output saved as .csv.

2) Python Data Processing:
Removed duplicates, handled missing values and data types.

Detected outliers.

Calculated "waves" based on course joining date.

Final dataset saved as .csv.

Visualized distributions and outliers.

3) Visualization (Yandex DataLens & Power BI):
Course Retention tab: retention analysis by course.

Students Overview tab: full table with filters by task requirements.

Retention funnel in Power BI.

Ability to export selected students for business purposes.

### Result:
✔️ Fully implemented end-to-end data analytics project.

✔️ Dashboards solve real business cases: search for students of a certain wave who did not renew a certain month of a specific course; compare retention between different types of courses; compile a list of students for further work with them.

✔️ Pipeline reflects actual data analyst workflow.
