from datetime import datetime

# Импорт библиотек
import pandas as pd
import duckdb as ddb
from IPython.display import display
import seaborn as sns
import matplotlib.pyplot as plt

# Задание таблиц БД
users = pd.read_csv('users.csv')
course_users = pd.read_csv('course_users.csv')
courses = pd.read_csv('courses.csv')
course_types = pd.read_csv('course_types.csv')
lessons = pd.read_csv('lessons.csv')
subjects = pd.read_csv('subjects.csv')
cities = pd.read_csv('cities.csv')
homework_done = pd.read_csv('homework_done.csv')
homework = pd.read_csv('homework.csv')
homework_lessons = pd.read_csv('homework_lessons.csv')
user_roles = pd.read_csv('user_roles.csv') 

# Создание запроса к базе данных
query = """
WITH courses_info AS 
(SELECT c.id as course_id, c.name as course_name, c.starts_at as course_start_date, 
s.id as subject_id, s.name as subject_name, s.project as subject_type,
c_t.id as course_type_id, c_t.name as course_type_name, c.lessons_in_month as les_mon
FROM courses c inner join subjects s on c.subject_id = s.id
inner join course_types c_t on c.course_type_id = c_t.id
),

users_info AS
(SELECT u.id as user_id, u.last_name as user_last_name, cit.id as city_id, cit.name as city_name, 
c_u.active as student_not_expelled, c_u.created_at as course_opening_date, c_u.course_id as c_id,
c_u.available_lessons as av_les
FROM users u left join cities cit on u.city_id = cit.id
inner join user_roles u_r on u.user_role_id = u_r.id
inner join course_users c_u on u.id = c_u.user_id
WHERE u_r.name = 'student'),

homework_info AS
(SELECT user_id as u_id, l.course_id as c_id, count(hw_d.id) as homework_done_on_course_by_user
FROM homework_done hw_d inner join homework_lessons hw_l on hw_d.homework_id = hw_l.homework_id
inner join lessons l on hw_l.lesson_id = l.id
GROUP BY u_id, c_id)

SELECT course_id, course_name, subject_id, subject_name, subject_type, course_type_id, course_start_date, user_id,
user_last_name, city_id, city_name, student_not_expelled, course_opening_date, 
av_les/NULLIF(les_mon, 0)::int as user_course_month_count, homework_done_on_course_by_user
FROM users_info u_i inner join courses_info c_i on u_i.c_id = c_i.course_id
left join homework_info h_i on h_i.u_id = u_i.user_id AND h_i.c_id = c_i.course_id
ORDER BY course_id
"""

# Выполнение SQL-запроса
df_result = ddb.query(query).to_df()

# Определим типы данных, проверим количество строк и столбцов, обнаружим столбцы с пропусками
df_result.info()
df_result.head(20)

# Обработка пропусков
# Не по всем ученикам есть информация о городе, видимо, это необязательная информация, заменим пропуски на 0 для айди и на "нет данных" для названия
df = df_result
df['city_id'] = df_result['city_id'].fillna(0)
df['city_name'] = df_result['city_name'].fillna('нет данных')
# Количество месяцев на курсе также заполнено не для всех пользователей. Полагаю, некоторые пользователи не открыли ни одного урока, дело в этом, соответственно, заменим пропускина нули
df['user_course_month_count'] = df_result['user_course_month_count'].fillna(0)
# Количество выполненных домашних заданий на курсе также содержит пропуски, что означает отсутствие выполненных д/з, заменяем пропуски на нули
df['homework_done_on_course_by_user'] = df_result['homework_done_on_course_by_user'].fillna(0)

# Обработка типов данных
# Все поля id должны быть целочисленными, однако айди города почему-то имеет тип float, проверим, что в этом столбце нет нецелых значений
print((df['city_id'] % 1 != 0).sum())
# Получили 0, значит, можем изменить тип данных на int64
df['city_id'] = df['city_id'].astype('int64')
# Проверим, есть ли НЕ целые числа в столбце с количеством месяцев
print((df['user_course_month_count'] % 1 != 0).sum())
# Получили 0, значит, можем изменить тип данных на int64
df['user_course_month_count'] = df['user_course_month_count'].astype('int64')

# Столбцы с названием курса, названием и типом предмета, фамилией пользователя и названием города преобразуем в строковый тип,
# но для начала проверим, что тип данных действительно строковый в этих столбцах
print(df['course_name'].apply(lambda x: isinstance(x, str)).all())
print(df['subject_name'].apply(lambda x: isinstance(x, str)).all())
print(df['subject_type'].apply(lambda x: isinstance(x, str)).all())
print(df['user_last_name'].apply(lambda x: isinstance(x, str)).all())
print(df['city_name'].apply(lambda x: isinstance(x, str)).all())
# Все значения True, значит, можем спокойно выполнить преобразование
df['course_name'] = df['course_name'].astype("string")
df['subject_name'] = df['subject_name'].astype("string")
df['subject_type'] = df['subject_type'].astype("string")
df['user_last_name'] = df['user_last_name'].astype("string")
df['city_name'] = df['city_name'].astype("string")

# Теперь остаётся проверить, все ли данные в столбцах с датами являются датами, и провести соответствующие преобразования
print(df['course_start_date'].apply(lambda x: isinstance(x, (pd.Timestamp, datetime))).all())
print(df['course_opening_date'].apply(lambda x: isinstance(x, (pd.Timestamp, datetime))).all())
# Это не даты, возможно, это тоже строки
print(df['course_start_date'].apply(lambda x: isinstance(x, (pd.Timestamp, str))).all())
print(df['course_opening_date'].apply(lambda x: isinstance(x, (pd.Timestamp, str))).all())
# да, строки, преобразуем их в даты-время и проверим, есть ли неудачно преобразованные строки
df['course_start_date'] = pd.to_datetime(df['course_start_date'], errors='coerce')
df['course_opening_date'] = pd.to_datetime(df['course_opening_date'], errors='coerce')
print(df[df['course_start_date'].isna()])
print(df[df['course_opening_date'].isna()])

# Преобразуем также тип данных столбца "студент не отчислен" к логическому с предварительной заменой 1 и 0
df['student_not_expelled'] = df['student_not_expelled'].apply(
    lambda x: True if x == 1
    else False if x == 0
    else pd.NA
)
print(df[df['student_not_expelled'].isna()])


# Проверка на наличие дубликатов
print(df.duplicated().sum())
# Дубликатов не обнаружено

# Анализ аномальных значений (выбросов)
# Посмотрим описательную статистику
print(df.describe())
# Буду использовать визуальную проверку с помощью "ящика с усами" и метод межквартильного размаха при необходимости
# для обнаружения выбросов, интересуют такие показатели, как дата старта курса, дата записи на курс, количество
# месяцев курса и количество выполненных домашних заданий на курсе
sns.boxplot(x=df['course_start_date'])  # выбросы — это точки за усами
plt.show()
# Судя по графику, обнаружено довольно много выбросов по дате старта курса, если более ранние даты меня не беспокоят,
# т.к. соответствуют датам в других таблицах (например, есть домашние задания от июня 2024), то курс с датой 11.2025
# вызывает подозрения
Q1 = df['course_start_date'].quantile(0.25)
Q3 = df['course_start_date'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['course_start_date'] > upper_bound)]
display(outliers)
# Видим, что на этом курсе указана дата записи на курс 4.11.2024, т.е. это описка, заменим год на 2024
df.loc[df['course_start_date'] == '2025-11-06', 'course_start_date'] = pd.to_datetime('2024-11-06')
# Проверяем, что выброс исчез
sns.boxplot(x=df['course_start_date'])  # выбросы — это точки за усами
plt.show()
# и проверяем на выбросы другие столбцы
sns.boxplot(x=df['course_opening_date'])
plt.show()
# Выбросов не обнаружено
sns.boxplot(x=df['user_course_month_count'])
plt.show()
# Значений больше 12 не обнаружено, а т.к. у нас годовые курсы, считаем, что выбросов нет
sns.boxplot(x=df['homework_done_on_course_by_user'])
plt.show()
# Может ли быть на курсе от 17 до 35 домашних заданий? Выведем строки с выбросами
Q1 = df['homework_done_on_course_by_user'].quantile(0.25)
Q3 = df['homework_done_on_course_by_user'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['homework_done_on_course_by_user'] > upper_bound)]
display(outliers)
# Как видно, таких значений достаточно много, не считаю их выбросами
# Деление учеников на волны проведём строго по дням с помощью отдельной функции
# Создадим (а после удалим) дополнительный столбец, в котором будет содержаться количество дней между присоединением ученика к курсу и началом курса (в виде целого числа int64)
df['days_between'] = (df['course_opening_date'] - df['course_start_date']).dt.days

# Создадим колонку с номером волны и запишем туда результат сравнения, используя функцию
def waves(days):
    if days <= 0:
        return 0
    elif days <= 7:
        return 1
    elif days <= 14:
        return 2
    elif days <= 21:
        return 3
    elif days <= 28:
        return 4
    else:
        return 5

df['wave'] = df['days_between'].apply(waves)
# Отобразим каждую волну
display(df[df['wave'] == 5].sort_values(by='days_between'))
# Отобразим итоговый результат, удалив лишнюю колонку
df.drop(columns='days_between', inplace=True)
display(df)
# Сохраним в формате csv для загрузки в Yandex DataLens
df.to_csv('test_dataset.csv', index=False)