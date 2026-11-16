# Online Education Course Continuation Analysis / Анализ продолжения обучения на онлайн-курсах


## 🇬🇧 English Description

### Project Goal

Building an end-to-end data analytics pipeline to analyze student course continuation and course access patterns in an online education platform:

1. Data extraction using SQL.
2. Data preprocessing and analysis using Python.
3. Interactive dashboard development in Power BI.

### Project Stages

**1. Data Extraction (SQL)**

- Extracted course, student, enrollment, and homework completion data.
- Used Common Table Expressions (CTEs) to improve query readability and structure.
- Applied JOIN operations to combine data from multiple tables.
- Saved the extracted dataset in CSV format.

**2. Data Preprocessing and Analysis (Python)**

- Checked for duplicate records, missing values, data type inconsistencies, and outliers.
- Handled missing values and converted data types.
- Identified and investigated potential data anomalies.
- Segmented students into enrollment waves based on the difference between the course start date and the course access opening date.
- Analyzed data distributions and potential outliers using visualizations.
- Prepared the final dataset for further analysis.

**3. Data Visualization (Power BI)**

The dashboard consists of two pages:

- **Course Continuation:** analyzes student continuation across course months, presents a funnel showing the number and percentage of students reaching each month, and enables comparisons across courses.
- **Student Information:** provides a student-level table with filters for enrollment status, course, enrollment wave, city, completed homework assignments, and the last course month reached.

The dashboard supports interactive filtering and student list exports for further analysis.

### Project Results

- Implemented an end-to-end analytics pipeline, from data extraction to interactive visualization.
- Developed a dashboard to compare course continuation patterns and identify stages with the largest declines in student numbers.
- Enabled the identification of students from specific enrollment waves who have not reached a selected course month.
- Provided a foundation for student segmentation and preparing targeted lists for further sales and student support activities.

**Note:** Course continuation is measured using available course access and enrollment data. It does not represent confirmed subscription renewals or payments.

---

## 🇷🇺 Описание проекта

### Цель проекта

Разработка полного аналитического цикла для оценки продолжения обучения и использования доступа к курсам онлайн-школы:

1. Извлечение данных из базы данных с помощью SQL.
2. Предобработка и анализ данных с использованием Python.
3. Создание интерактивного дашборда в Power BI.

### Этапы проекта

**1. Извлечение данных (SQL)**

- Выгрузка данных о курсах, студентах, записях на курсы и выполненных домашних заданиях.
- Использование Common Table Expressions (CTE) для повышения читаемости и структурирования запроса.
- Применение JOIN для объединения таблиц.
- Результат сохранён в формате CSV.

**2. Предобработка и анализ данных (Python)**

- Проверка данных на дубликаты, пропуски, корректность типов данных и выбросы.
- Обработка пропущенных значений и преобразование типов данных.
- Выявление и проверка потенциальных аномалий.
- Сегментация студентов на волны в зависимости от даты открытия доступа относительно даты начала курса.
- Анализ распределений и потенциальных выбросов с помощью визуализаций.
- Подготовка итогового датасета для дальнейшего анализа.

**3. Визуализация данных (Power BI)**

Дашборд состоит из двух страниц:

- **Course Continuation:** анализ продолжения обучения по месяцам, воронка количества и доли студентов, достигших каждого месяца курса, сравнение показателей по курсам.
- **Student Information:** таблица с информацией о студентах и фильтрами по статусу, курсу, волне, городу, количеству выполненных домашних заданий и последнему достигнутому месяцу курса.

Предусмотрена возможность фильтрации и выгрузки списков студентов для дальнейшего анализа.

### Результаты проекта

- Реализован полный аналитический цикл: от извлечения данных до интерактивной визуализации.
- Дашборд позволяет сравнивать продолжение обучения на разных курсах и выявлять этапы, на которых количество студентов сокращается.
- Реализована возможность находить студентов определённой волны, не достигших выбранного месяца курса.
- Подготовлена основа для сегментации студентов и формирования списков для дальнейшей работы отдела продаж и поддержки.
