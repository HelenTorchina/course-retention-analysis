# SQL Data Extraction

The database schema is provided in `db_schema_english.jpg`. The database is populated from CSV files using a Python script.

The SQL query uses Common Table Expressions (CTEs) to improve readability and organize the data extraction process into logical steps.

## 1. `courses_info`

This CTE retrieves course-related information by joining three tables:

- `courses`: course ID, course name, and course start date;
- `subjects`: subject ID, subject name, and subject type;
- `course_types`: course type ID, course type name, and the number of lessons per month.

All joins are `INNER JOIN` operations because the source database contains no courses without an associated subject or course type.

## 2. `users_info`

This CTE retrieves student and course enrollment information:

- `users`: student ID and last name;
- `cities`: city ID and city name;
- `user_roles`: user role, used to filter records and include students only;
- `course_users`: course enrollment status, course access opening date, course ID, and the number of available lessons.

The `cities` table is joined using a `LEFT JOIN` because some users do not have a city specified in the database. The `user_roles` table is joined using an `INNER JOIN`, and the query filters records by the `student` role.

## 3. `homework_info`

This CTE calculates the number of completed homework assignments for each student on each course.

It combines the `homework_done`, `homework_lessons`, and `lessons` tables, counts completed homework records, and groups the results by student ID and course ID.

All joins are `INNER JOIN` operations. This ensures that only homework records linked to lessons and courses are included in the resulting dataset.

## 4. Final Query

The final query combines the results of all three CTEs to produce a dataset containing course, student, enrollment, and homework information.

It also calculates the number of full months of course access available to each student by dividing the number of available lessons by the number of lessons scheduled per month. `NULLIF` is used to prevent division by zero.

The resulting dataset serves as the basis for further analysis in Python and Power BI.
