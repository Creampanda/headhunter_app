from app import db
from parsing_functions import parse_all
from config import API_URL
from psycopg2.extras import NamedTupleCursor, DictCursor


def parse_latest_and_save(start_area, end_area, i, j):
    with db, db.cursor(cursor_factory=NamedTupleCursor) as cur:
        for vacancy_dict in parse_all(
            API_URL, latest_only=False, start_area=start_area, end_area=end_area, i=i, j=j
        ):
            cur.execute(
                """
                INSERT INTO vacancies
                    (
                    vacancy_id, vacancy_name, profession, \
                    industry, experience, key_skills, \
                    employer, area, salary_from, salary_to, \
                    currency, job_description, published_at, \
                    created_at, archived, employment_type, vacancy_url
                    )
                VALUES (%s, %s, %s,%s, %s, %s,%s, %s, \
                        %s, %s,%s, %s, %s,%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                tuple(vacancy_dict.values()),
            )
            cur.execute("COMMIT")


parse_latest_and_save(start_area=10, end_area=-1, i=0, j=-1)