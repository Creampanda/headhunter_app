\set passw `echo $POSTGRES_PASSWORD`
-- \connect dbname=hints user=hints password= :passw
\c hints hints
drop table if exists vacancies cascade;
create table vacancies (
    vacancy_id integer not null primary key,
    vacancy_name text not null,
    profession text not null,
    industry text not null,
    experience text not null,
    key_skills text[],
    employer text not null,
    area text not null,
    salary_from text,
    salary_to text,
    currency text,
    job_description text,
    published_at timestamptz  not null,
    created_at timestamptz  not null,
    archived boolean,
    employment_type text,
    vacancy_url text not null
);