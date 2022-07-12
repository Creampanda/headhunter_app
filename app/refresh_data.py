from app import db
from parsing_functions import Parser
from random import random
from time import sleep
from psycopg2.extras import NamedTupleCursor, DictCursor


def _select_item_no_descr(cur):
    cur.execute(
        """
        SELECT vacancy_id
        FROM vacancies
        WHERE job_description is null
        LIMIT 1 FOR UPDATE SKIP LOCKED
        """
    )
    res = cur.fetchall()
    if not res:
        return
    assert len(res) == 1
    return res[0]


def update_vacancy(proxies):
    parser = Parser(proxies)
    parser.set_proxy()
    with db, db.cursor(cursor_factory=NamedTupleCursor) as cur:
        while True:
            vacancy_for_update_id = _select_item_no_descr(cur).vacancy_id
            print("Updating id=", vacancy_for_update_id)
            sleep(random() * 5)
            try:
                vacancy_dict = parser.parse_vacancy(vacancy_for_update_id)
            except Exception as e:
                print(e)
            else:
                if vacancy_dict is None:
                    cur.execute(
                        """
                        UPDATE vacancies
                        SET job_description= %s
                        WHERE vacancy_id = %s;
                        """,
                        ("Not found", vacancy_for_update_id),
                    )
                else:
                    cur.execute(
                        """
                        UPDATE vacancies
                        SET profession= %(profession)s,
                            experience= %(experience)s,
                            key_skills= %(key_skills)s,
                            job_description= %(job_description)s,
                            employment= %(employment)s,
                            archived= %(archived)s
                        WHERE vacancy_id = %(vacancy_id)s;
                        """,
                        vacancy_dict,
                    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proxies", type=str, nargs="+", help="")
    args = parser.parse_args()
    update_vacancy(**vars(args))
