1. common

Umumiy ma'lumotnomalar. Boshqa applar shularni ishlatadi.

Region: name, parent (viloyat → tuman)
Category: name, slug, parent (IT → Backend)
Skill: name

2. users
User: email (login), phone, role (candidate / employer), is_verified

3. companies
Company: owner (User), name, logo, description, website, region, employees_count, is_verified

4. resumes
Resume: user, title, category, region, expected_salary, currency, about, skills (M2M), is_public
Education: resume, institution, specialty, degree, start_year, end_year
WorkExperience: resume, company_name, position, start_date, end_date, is_current, description
Language: resume, name, level

5. vacancies
Vacancy: company, title, category, region, description, requirements, salary_from, salary_to, currency, experience, employment_type, skills (M2M), status (draft / active / archived), published_at, expires_at
FavoriteVacancy: user, vacancy

6. applications
Application: vacancy, resume, cover_letter, status (new / viewed / invited / rejected)
Bir rezyume bir vakansiyaga faqat bir marta murojaat qila oladi (unique vacancy + resume).
Keyinroq qo'shiladigan app

notifications: Notification (xabarnomalar). Xohlasangiz yozishma uchun Message modeli ham shu yerga qo'shiladi.