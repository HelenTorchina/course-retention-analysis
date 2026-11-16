from datetime import datetime

# Import required libraries
import pandas as pd
import duckdb as ddb
from IPython.display import display
import seaborn as sns
import matplotlib.pyplot as plt

# Load database tables from CSV files
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

# Define SQL query for data extraction
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

# Execute SQL query and convert the result to a DataFrame
df_result = ddb.query(query).to_df()

# Inspect data types, dataset dimensions, and missing values
df_result.info()
df_result.head(20)

# Handle missing values
# Replace missing city IDs with 0 and missing city names with 'Unknown' ("нет данных")
df = df_result
df['city_id'] = df_result['city_id'].fillna(0)
df['city_name'] = df_result['city_name'].fillna('нет данных')
# Replace missing course access duration with 0
df['user_course_month_count'] = df_result['user_course_month_count'].fillna(0)
# Replace missing homework counts with 0
df['homework_done_on_course_by_user'] = df_result['homework_done_on_course_by_user'].fillna(0)

# Convert data types
# Check for non-integer values in the city ID column
print((df['city_id'] % 1 != 0).sum())
# No non-integer values found; convert city IDs to int64
df['city_id'] = df['city_id'].astype('int64')
# Check for non-integer values in the course access duration column
print((df['user_course_month_count'] % 1 != 0).sum())
# No non-integer values found; convert course access duration to int64
df['user_course_month_count'] = df['user_course_month_count'].astype('int64')

# Validate string values before converting columns to the string data type
print(df['course_name'].apply(lambda x: isinstance(x, str)).all())
print(df['subject_name'].apply(lambda x: isinstance(x, str)).all())
print(df['subject_type'].apply(lambda x: isinstance(x, str)).all())
print(df['user_last_name'].apply(lambda x: isinstance(x, str)).all())
print(df['city_name'].apply(lambda x: isinstance(x, str)).all())
# All values are strings; convert the relevant columns to the string data type
df['course_name'] = df['course_name'].astype("string")
df['subject_name'] = df['subject_name'].astype("string")
df['subject_type'] = df['subject_type'].astype("string")
df['user_last_name'] = df['user_last_name'].astype("string")
df['city_name'] = df['city_name'].astype("string")

# Validate and convert date columns
# Check whether date columns contain datetime values
print(df['course_start_date'].apply(lambda x: isinstance(x, (pd.Timestamp, datetime))).all())
print(df['course_opening_date'].apply(lambda x: isinstance(x, (pd.Timestamp, datetime))).all())
# Date values are stored as strings; verify their data types
print(df['course_start_date'].apply(lambda x: isinstance(x, (pd.Timestamp, str))).all())
print(df['course_opening_date'].apply(lambda x: isinstance(x, (pd.Timestamp, str))).all())
# Convert date columns to datetime and check for parsing errors
df['course_start_date'] = pd.to_datetime(df['course_start_date'], errors='coerce')
df['course_opening_date'] = pd.to_datetime(df['course_opening_date'], errors='coerce')
print(df[df['course_start_date'].isna()])
print(df[df['course_opening_date'].isna()])

# Convert the student enrollment status column to Boolean
# Map 1 to True, 0 to False, and other values to missing
# Check for missing values after conversion
df['student_not_expelled'] = df['student_not_expelled'].apply(
    lambda x: True if x == 1
    else False if x == 0
    else pd.NA
)
print(df[df['student_not_expelled'].isna()])


# Check for duplicate records
print(df.duplicated().sum())
# No duplicate records found

# Detect potential outliers
# Review descriptive statistics
print(df.describe())
# Use boxplots and the interquartile range (IQR) method to identify potential outliers
# Check course start dates for potential outliers
sns.boxplot(x=df['course_start_date']) 
plt.show()
# Earlier dates are consistent with dates in other tables and are retained
# Investigate the course with the November 2025 start date
Q1 = df['course_start_date'].quantile(0.25)
Q3 = df['course_start_date'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['course_start_date'] > upper_bound)]
display(outliers)
# The enrollment date indicates a likely data entry error; correct the year to 2024
df.loc[df['course_start_date'] == '2025-11-06', 'course_start_date'] = pd.to_datetime('2024-11-06')
# Verify the correction
sns.boxplot(x=df['course_start_date'])
plt.show()
# Check enrollment dates for potential outliers
sns.boxplot(x=df['course_opening_date'])
plt.show()
# No significant outliers detected
sns.boxplot(x=df['user_course_month_count'])
plt.show()
# Check course access duration for potential outliers
# No values above 12 months found; the dataset contains annual courses
sns.boxplot(x=df['homework_done_on_course_by_user'])
plt.show()
# Check completed homework counts for potential outliers
# Review records with unusually high homework counts
Q1 = df['homework_done_on_course_by_user'].quantile(0.25)
Q3 = df['homework_done_on_course_by_user'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['homework_done_on_course_by_user'] > upper_bound)]
display(outliers)
# These values are relatively frequent and are not treated as outliers

# Segment students into enrollment waves based on the number of days
# between the course start date and the course access opening date
# Calculate the difference in days
df['days_between'] = (df['course_opening_date'] - df['course_start_date']).dt.days

# Assign enrollment wave labels based on the number of days after the course start date
def waves(days):
    if pd.isna(days): # Missing dates are retained as missing wave values
        return pd.NA
    if days <= 0: # Wave 0: on or before the course start date
        return 0
    elif days <= 7: # Wave 1: 1–7 days after the start date
        return 1
    elif days <= 14: # Wave 2: 8–14 days after the start date
        return 2
    elif days <= 21: # Wave 3: 15–21 days after the start date
        return 3
    elif days <= 28: # Wave 4: 22–28 days after the start date
        return 4
    else:             # Wave 5: more than 28 days after the start date
        return 5

df['wave'] = df['days_between'].apply(waves).astype('Int64')
# Review students assigned to Wave 5
display(df[df['wave'] == 5].sort_values(by='days_between'))
# Remove the temporary column and display the final dataset
df.drop(columns='days_between', inplace=True)
display(df)
# Export the processed dataset to CSV for use in Power BI and Yandex DataLens
df.to_csv('test_dataset.csv', index=False)
