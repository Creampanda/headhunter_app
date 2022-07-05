\set passw `echo $POSTGRES_PASSWORD`
-- \connect dbname=hints user=hints password= :passw
\c hints hints
drop table if exists vacancies cascade;
create table vacancies (
    vacancy_id integer not null primary key,
    vacancy_name text not null,
    profession text,
    industry text,
    experience text,
    key_skills text[],
    employer text,
    area text,
    salary_from text,
    salary_to text,
    currency text,
    job_description text,
    published_at timestamptz,
    created_at timestamptz,
    archived boolean,
    employment_type text,
    vacancy_url text not null
);