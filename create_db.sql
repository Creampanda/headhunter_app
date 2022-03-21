\set thepassword `echo $POSTGRES_PASSWORD`
drop database if exists hints;
drop user if exists hints;

create database hints;
create user hints with encrypted password :'thepassword';
grant all privileges on database hints to hints;
-- grant all privileges on all tables in schema public to hints;
-- postgresql://hints:56rVCKMedQd8LFnDRgiuuy@localhost/hints?connect_timeout=5

\connect hints