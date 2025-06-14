# Описание дашбордов

Разделила дашборды на две вкладки: Продления курсов и Ученики курсов. 
Самую большую сложность вызвали чарты с числом и процентом учеников, продливших курс. 
Для создания этих чартов пришлось организовать несколько переменных по формулам:

Reached Month i: if([user_course_month_count] >= i, 1, 0),
i: sum([Reached Month i]), i=(0,11) 

Проценты считались по формулам:
i месяцев: SUM([Reached Month i])/SUM([Reached Month 0])*100, i=(0,11) 

## Yandex DataLens
Ссылка на дашборд в Yandex DataLens: https://datalens.yandex/2f9bh3b07pcgo.

### Вкладка 1: Продления курсов

**Цель:**  
Анализ продлений курсов учениками.

**Основные элементы:**
- Таблицы с количеством и процентом продлений для выбранных курсов.
- Линейный график числа продлений по месяцам.
- Линейный график процентного соотношения продлений.
- Фильтр выбора курсов (множественный выбор).

**Пример анализа:**
см. файл Продления курсов.png в datalens_screenshots

Мы выбрали ряд курсов для сравнения. 
Из таблицы слева можем увидеть, что эта группа курсов в совокупности привлекла более 5 тысяч учеников, а трое из них дошли до 10-го месяца. 

Из таблицы справа видим, какой процент учеников в этой группе курса до какого месяца обучения добрался.

Из нижнего левого графика можем сделать вывод о том, что внутри выбранной группы самым популярным курсом является Годовой 2к25 стандарт, на него записались более 4 тысяч учеников, большая часть которых продлила первый и второй месяцы обучения, 250 учеников продлили месяцы вплоть до 9-го, а трое – до десятого месяца.

Из нижнего правого чарта мы видим проценты продления и понимаем, что хуже всего продлевался Годовой курс 2к25 с Катей, т.к. по сравнению с остальными курсами группы процент продлений второго месяца минимален.

### Вкладка 2: Ученики курсов

**Цель:**  
Отбор учеников для работы отдела продаж/поддержки.

**Основные элементы:**
- Таблица со всеми данными по ученикам:
- Курс;
- Волна;
- Город;
- Статус отчисления;
- Количество сданных ДЗ;
- Последний продлённый месяц.

- Фильтры:
- Статус "не отчислен";
- Название курса;
- Номер волны;
- Город;
- Минимальное число сданных ДЗ;
- Последний продлённый месяц курса.

**Пример анализа:**
см. файл Ученики курсов.png в datalens_screenshots

Пусть нам нужны ученики 3-ей волны, не продлившие по какой-то причине 4-й месяц самого популярного нашего курса Годовой 2к25 стандарт. 

Нас интересуют только НЕ отчисленные ученики, поэтому ставим галочку в чек-боксе, также выбираем соответствующий курс, соответствующую волну и ставим 2 в окне с последним продлённым месяцем. 

Полученную таблицу можно отсортировать удобным образом и, например, скачать в Excel для дальнейшего анализа. 

## Power BI
Содержится в файле «Студенты курсов.pbix». Как и в варианте Yandex DataLens, есть деление на две вкладки с теми же названиями. 
Плюс этого инструмента в возможности показать воронку, используя имеющиеся данные, где сразу отображаются и число, и проценты, и есть наглядное деление по месяцам (на первой вкладке).

### Вкладка 1: Продления курсов (Course Retention)
**Цель:** Анализ воронки продлений.

**Основные элементы:**
- Воронка по месяцам продления: показывает абсолютные значения и проценты.
- Таблица с детализацией по каждому курсу.
- Фильтр выбора курсов.

### Вкладка 2: Ученики курсов (Students Overview)
**Цель:** Формирование списков учеников для работы.

**Основные элементы:**
- Таблица с данными о студентах.
- Фильтры:
- Статус отчисления;
- Курс;
- Волна;
- Город;
- Последний продлённый месяц;
- Количество выполненных ДЗ.

**Пример анализа:**
Исходя из общих данных по выбранной группе курсов, мы можем сделать вывод, что студент, продливший 4 месяца курса группы, 
с высокой вероятностью продлит все месяцы вплоть до 9-го, а вот 10-й месяц и далее почти не продляют. 
см. файл Продления курсов с фильтрацией.png в powerbi_screenshots

Мы можем пожелать выяснить причины, связавшись со студентами, не продлившими курс. 
Чтобы их найти, введём соответствующие фильтры во вторую вкладку:
- перечислим выбранные курсы;
- в селекторе Не продлили данный месяц выберем 10.
Если из этой выборки интересуют, например, только московские студенты 3-й волны, выберем также соответствующие значения по городу и волне и получим готовый список интересующих нас студентов.
см. файл Ученики курсов.png в powerbi_screenshots


## Вывод / Conclusion

- Дашборды позволяют анализировать поведение учеников на курсах по продлениям.
- Есть возможность выбрать конкретных учеников для маркетинговых или поддерживающих активностей.
- Все фильтры работают гибко и удобно для пользователей.
