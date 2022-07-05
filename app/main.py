from app import db
from parsing_functions import Parser
from psycopg2.extras import NamedTupleCursor, DictCursor


def parse_latest_and_save(proxies, start, end, search_period):
    # print(proxies, start, end, search_period)
    # print(type(proxies), type(start), type(end), type(search_period))
    
    parser = Parser(proxies, start, end, search_period)
    with db, db.cursor(cursor_factory=NamedTupleCursor) as cur:
        for vacancy_dict in parser.parse_all():
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proxies", type=str, nargs="+", help="")
    parser.add_argument("-start", type=int, help="", default=0)
    parser.add_argument("-end", type=int, help="", default=-1)
    parser.add_argument("-search_period", type=int, help="", default=0)
    args = parser.parse_args()
    parse_latest_and_save(**vars(args))
