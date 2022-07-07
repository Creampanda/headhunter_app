from app import db

from parsing_functions import Parser
from psycopg2.extras import NamedTupleCursor, DictCursor
from time import sleep
import requests
import fake_useragent



vacancy = _select_item()
print(vacancy.vacancy_id)
vacancy_url = f"https://api.hh.ru/vacancies/{vacancy.vacancy_id}"

session = requests.Session()
user = fake_useragent.UserAgent().random
user = user
header = {"user_agent": user}
resp = session.get(vacancy_url, headers=header)
assert resp.status_code == 200
resp.encoding = "utf-8"
data = resp.json()
desc = data["description"]
desc = BeautifulSoup(desc, "lxml").text.strip()
experience = data["experience"]["id"]
key_skills_dict = data["key_skills"]
key_skills = []
for skill in key_skills_dict:
    key_skills.append(skill["name"])
profession = data["professional_roles"][0]["name"]


def update_vacancy(
profession,
key_skills,
experience,
desc,
vacancy.vacancy_id);

with db, db.cursor(cursor_factory=NamedTupleCursor) as cur:
    cur.execute(
        """
            UPDATE vacancies
            SET profession = %(profession)s,
                key_skills = %(key_skills)s,
                experience = %(experience)s,
                job_description = %(description)s
            WHERE vacancy_id = %(vacancy_id)s
        """,
        {
            "profession":  profession,
            "key_skills":  key_skills,
            "experience":  experience,
            "description": desc,
            "vacancy_id":  vacancy.vacancy_id,
        },
    )
