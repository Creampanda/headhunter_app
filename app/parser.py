from time import sleep
import requests
import fake_useragent
from random import random
from config import *
from bs4 import BeautifulSoup

import os
import psycopg2


class Parser:
    def __init__(self, proxies, start_area=0, end_area=-1, search_period=0) -> None:
        self.session = requests.Session()
        user = fake_useragent.UserAgent().random
        self.header = {"user_agent": user}
        self.url = API_URL
        self.proxies = proxies
        self.areas = AREA_IDS[start_area:end_area]
        self.search_period = search_period
        db_connstring = os.getenv("HINTS_DB_CONNSTRING")
        self.db = psycopg2.connect(db_connstring)

    def set_proxy(self):
        proxy = self.proxies.pop(0)
        print("========================================")
        print("Trying via: " + proxy)
        print("========================================")
        self.session = requests.Session()
        user = fake_useragent.UserAgent().random
        self.header = {"user_agent": user}
        self.session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        sleep(1)
        resp = self.session.get(API_URL)
        assert resp.status_code == 200, resp.text
        resp = self.session.get("https://httpbin.org/ip")
        assert resp.status_code == 200, resp.text
        print("========================================")
        print("Connected via: " + resp.json()["origin"])
        print("========================================")
        self.proxies.append(proxy)

    def get_response_json(self, params=None, custom_url=None):
        url = custom_url if custom_url else self.url
        resp = self.session.get(url, headers=self.header, params=params)
        if (
            resp.json().get("errors") == [{"type": "not_found"}]
            and resp.status_code == 404
        ):
            print("Description not found...", end="\r")
            return None
        assert resp.status_code == 200, resp.text
        resp.encoding = "utf-8"
        return resp.json()

    def get_and_save_by_params(self, params):
        try:
            data = self.get_response_json(params)
        except Exception:
            self.set_proxy()
            data = self.get_response_json(params)
        if not data.get("pages") or not data.get("items"):
            # print("========================================")
            # print(data.keys())
            # print("========================================")
            try:
                data = self.get_response_json(params)
            except Exception:
                self.set_proxy()
                data = self.get_response_json(params)

        total_pages = data["pages"]
        for i in range(total_pages):
            sleep(random() * 5)
            params["page"] = i
            if i > 0:
                data = self.get_response_json(params)

            for vacancy in data["items"]:
                try:
                    vacancy_name = vacancy["name"]
                except Exception:
                    vacancy_name = None
                try:
                    area = vacancy["area"]["name"]
                except Exception:
                    area = None
                try:
                    employer = vacancy["employer"]["name"]
                except Exception:
                    employer = None
                try:
                    salary_from = vacancy["salary"]["from"]
                except Exception:
                    salary_from = None
                try:
                    salary_to = vacancy["salary"]["to"]
                except Exception:
                    salary_to = None
                try:
                    currency = vacancy["salary"]["currency"]
                except Exception:
                    currency = None
                try:
                    published_at = vacancy["published_at"]
                except Exception:
                    published_at = None
                try:
                    created_at = vacancy["created_at"]
                except Exception:
                    created_at = None
                try:
                    archived = vacancy["archived"]
                    if archived is False:
                        archived = None
                except Exception:
                    archived = None
                try:
                    schedule = vacancy["schedule"]["name"]
                except Exception:
                    schedule = None
                try:
                    profession = PROFESSIONAL_ROLES_ALL[params["professional_role"]]
                except Exception:
                    profession = None
                try:
                    industry = INDUSTRIES[params["industry"]]
                except Exception:
                    industry = None
                try:
                    experience = params["experience"]
                except Exception:
                    experience = None
                try:
                    employment_type = params["employment"]
                except Exception:
                    employment_type = None

                vacancy_url = vacancy["alternate_url"]
                vacancy_id = vacancy_url.split("/")[-1]

                vacancy_dict = {
                    "vacancy_id": vacancy_id,
                    "vacancy_name": vacancy_name,
                    "profession": profession,
                    "industry": industry,
                    "experience": experience,
                    "key_skills": None,
                    "employer": employer,
                    "area": area,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "job_description": None,
                    "published_at": published_at,
                    "created_at": created_at,
                    "archived": archived,
                    "schedule": schedule,
                    "employment": employment_type,
                    "vacancy_url": vacancy_url,
                }
                yield vacancy_dict

    def parse_all(self):
        print(f"target areas: {self.areas[0]} ... {self.areas[-1]}", end="\r")
        self.set_proxy()
        for area in self.areas:
            params = dict()
            params["period"] = self.search_period
            sleep(random() * 5)
            params["area"] = area
            params["per_page"] = 100
            try:
                data = self.get_response_json(params)
            except Exception:
                self.set_proxy()
                data = self.get_response_json(params)
            print(f"Found {data['found']} vacancies for ", params, end="\r")
            if data["found"] == 0:
                continue
            if data["found"] <= 2000:
                for vacancy_dict in self.get_and_save_by_params(params=params):
                    yield vacancy_dict
            else:
                for professional_role_id in PROFESSIONAL_ROLES_ALL.keys():
                    sleep(random() * 5)
                    params["professional_role"] = professional_role_id
                    if params.get("employment"):
                        params.pop("employment")
                    if params.get("experience"):
                        params.pop("experience")
                    try:
                        data = self.get_response_json(params)
                    except Exception:
                        self.set_proxy()
                        data = self.get_response_json(params)
                    print(f"Found {data['found']} vacancies for ", params, end="\r")
                    if data["found"] == 0:
                        continue
                    if data["found"] <= 2000:
                        for vacancy_dict in self.get_and_save_by_params(params=params):
                            yield vacancy_dict
                    else:
                        for exp in EXPERIENCE:
                            sleep(random() * 5)
                            params["experience"] = exp
                            try:
                                data = self.get_response_json(params)
                            except Exception:
                                self.set_proxy()
                                data = self.get_response_json(params)
                            print(
                                f"Found {data['found']} vacancies for ",
                                params,
                                end="\r",
                            )
                            if data["found"] == 0:
                                continue
                            if data["found"] <= 2000:
                                for vacancy_dict in self.get_and_save_by_params(
                                    params=params
                                ):
                                    yield vacancy_dict
                            else:
                                for employment_type in EMPLOYMENT:
                                    sleep(random() * 5)
                                    params["employment"] = employment_type
                                    try:
                                        data = self.get_response_json(params)
                                    except Exception:
                                        self.set_proxy()
                                        data = self.get_response_json(params)
                                    print(
                                        f"Found {data['found']} vacancies for ",
                                        params,
                                        end="\r",
                                    )
                                    if data["found"] == 0:
                                        continue
                                    for vacancy_dict in self.get_and_save_by_params(
                                        params=params
                                    ):
                                        yield vacancy_dict

    def parse_vacancy(self, vacancy_id):
        vacancy_url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        try:
            data = self.get_response_json(custom_url=vacancy_url)
        except Exception as e:
            print(e)
            self.set_proxy()
            data = self.get_response_json(custom_url=vacancy_url)
        if data is None:
            return
        # print('data ', data)
        # import pdb;pdb.set_trace()
        desc = data["description"]
        desc = BeautifulSoup(desc, "lxml").text.strip()
        experience = data["experience"]["id"]
        key_skills_dict = data["key_skills"]
        key_skills = []
        for skill in key_skills_dict:
            key_skills.append(skill["name"])
        profession = data["professional_roles"][0]["name"]
        specializations = []
        for spec in data["specializations"]:
            specializations.append(spec["name"])
        employment_type = data["employment"]["id"]
        archived = data["archived"]
        vacancy_dict = {
            "vacancy_id": vacancy_id,
            "profession": profession,
            "experience": experience,
            "key_skills": key_skills,
            "job_description": desc,
            "employment": employment_type,
            "archived": archived,
        }
        return vacancy_dict

    def test(self):
        resp = self.get_response_json()
        print(resp.keys())
        self.set_proxy()
        resp = self.get_response_json()
        print(resp.keys())
        self.set_proxy()
        resp = self.get_response_json()
        print(resp.keys())


# def parse_developers():
#     params = {"area": 1, "professional_role": 96}
#     for industry in [7.538, 7.539, 7.540, 7.541]:
#         params["industry"] = industry
#         for exp in EXPERIENCE:
#             for exp in EXPERIENCE:
#                 # print(
#                 #     f"industry_id = {industry},\
#                 #     experience = {exp}"
#                 # )
#                 params["experience"] = exp
#                 resp = session.get(API_URL, headers=header, params=params)
#                 resp.encoding = "utf-8"
#                 data = json.loads(resp.text)
#                 print(f"Found {data['found']} vacancies for ", params)
#                 if data["found"] == 0:
#                     continue
#                 for vacancy in get_and_save_by_params(API_URL, params=params):
#                     yield vacancy
