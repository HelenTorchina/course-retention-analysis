WITH courses_info AS 
(SELECT c.id as course_id, c.name as course_name, 
c.starts_at as course_start_date, 
s.id as subject_id, s.name as subject_name, s.project as subject_type,
c_t.id as course_type_id, c_t.name as course_type_name, 
c.lessons_in_month as les_mon
FROM courses c 
inner join subjects s on c.subject_id = s.id
inner join course_types c_t on c.course_type_id = c_t.id
),

users_info AS
(SELECT u.id as user_id, u.last_name as user_last_name, 
cit.id as city_id, cit.name as city_name, 
c_u.active as student_not_expelled, 
c_u.created_at as course_opening_date, 
c_u.course_id as c_id,
c_u.available_lessons as av_les
FROM users u 
left join cities cit on u.city_id = cit.id
left join user_roles u_r on u.user_role_id = u_r.id
inner join course_users c_u on u.id = c_u.user_id
WHERE u_r.name = 'student'),

homework_info AS
(SELECT user_id as u_id, l.course_id as c_id, 
count(hw_d.id) as homework_done_on_course_by_user
FROM homework_done hw_d 
left join homework_lessons hw_l on hw_d.homework_id = hw_l.homework_id
left join lessons l on hw_l.lesson_id = l.id
GROUP BY u_id, c_id)

SELECT course_id, course_name, 
subject_id, subject_name, subject_type, 
course_type_id, course_start_date, 
user_id, user_last_name, 
city_id, city_name, 
student_not_expelled, 
course_opening_date, 
av_les/NULLIF(les_mon, 0) as user_course_month_count, 
homework_done_on_course_by_user
FROM users_info u_i 
inner join courses_info c_i on u_i.c_id = c_i.course_id
left join homework_info h_i on h_i.u_id = u_i.user_id AND h_i.c_id = c_i.course_id
ORDER BY course_id