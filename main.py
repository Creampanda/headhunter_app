from time import sleep
import requests
import fake_useragent
import json
from random import random

from config import *

session = requests.Session()
user = fake_useragent.UserAgent().random
header = {"user_agent": user}


API_URL = "https://api.hh.ru/vacancies"


def parse_developers():
    params = {"area": 1, "professional_role": 96}
    for industry in [7.538, 7.539, 7.540, 7.541]:
        params["industry"] = industry
        for exp in EXPERIENCE:
            for exp in EXPERIENCE:
                print(
                    f"industry_id = {industry},\
                    experience = {exp}"
                )
                params["experience"] = exp
                resp = session.get(API_URL, headers=header, params=params)
                resp.encoding = "utf-8"
                data = json.loads(resp.text)
                if data["found"] == 0:
                    continue
                for vacancy in get_and_save_by_params(API_URL, params=params):
                    yield vacancy


def get_and_save_by_params(url, params):
    resp = session.get(url, headers=header, params=params)
    resp.encoding = "utf-8"
    data = json.loads(resp.text)
    total_pages = data["pages"]
    for i in range(0, total_pages):
        sleep(random() * 5)
        params["page"] = i
        resp = session.get(url, headers=header, params=params)
        resp.encoding = "utf-8"
        data = json.loads(resp.text)
        for vacancy in data["items"]:
            try:
                vacancy_name = vacancy["name"]
            except:
                vacancy_name = None
            try:
                area = vacancy["area"]["name"]
            except:
                area = None
            try:
                employer = vacancy["employer"]["name"]
            except:
                employer = None
            try:
                salary_from = vacancy["salary"]["from"]
            except:
                salary_from = None
            try:
                salary_to = vacancy["salary"]["to"]
            except:
                salary_to = None
            try:
                currency = vacancy["salary"]["currency"]
            except:
                currency = None
            try:
                published_at = vacancy["published_at"]
            except:
                published_at = None
            try:
                created_at = vacancy["created_at"]
            except:
                created_at = None
            try:
                archived = vacancy["archived"]
            except:
                archived = None
            try:
                schedule = vacancy["schedule"]["name"]
            except:
                schedule = None

            vacancy_url = vacancy["alternate_url"]
            vacancy_dict = {
                "vacancy_name": vacancy_name,
                "profession": PROFESSIONAL_ROLES_ALL[params["professional_role"]],
                "industry": INDUSTRIES[params["industry"]],
                "experience": PROFESSIONAL_ROLES_ALL[params["professional_role"]],
                "employer": employer,
                "area": area,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "published_at": published_at,
                "created_at": created_at,
                "archived": archived,
                "schedule": schedule,
                "url": vacancy_url,
            }
            yield vacancy_dict


def parse_all(url, latest_only=False):
    params = dict()
    if latest_only:
        params["search_period"] = 1
    for area in AREA_IDS:
        sleep(random() * 5)
        params["area"] = area
        resp = session.get(url, headers=header, params=params)
        resp.encoding = "utf-8"
        data = json.loads(resp.text)
        print(f"area={area}, found={data['found']}")
        if data["found"] == 0:
            continue
        else:
            for professional_role_id in PROFESSIONAL_ROLES_ALL.keys():
                sleep(random() * 5)
                params["professional_role"] = professional_role_id
                resp = session.get(url, headers=header, params=params)
                resp.encoding = "utf-8"
                data = json.loads(resp.text)
                if data["found"] == 0:
                    continue
                else:
                    for industry_id in INDUSTRIES.keys():
                        if (
                            area == 1
                            and professional_role_id == 96
                            and industry_id == 7
                            and not latest_only
                        ):
                            continue
                        print(
                            f"area={area}, \
                            profession_id = {professional_role_id}, \
                            industry_id = {industry_id}"
                        )
                        params["industry"] = industry_id
                        resp = session.get(url, headers=header, params=params)
                        resp.encoding = "utf-8"
                        data = json.loads(resp.text)
                        if data["found"] == 0:
                            continue
                        else:
                            for exp in EXPERIENCE:
                                print(
                                    f"area={area},\
                                    profession_id = {professional_role_id},\
                                    industry_id = {industry_id},\
                                    experience = {exp}"
                                )
                                params["experience"] = exp
                                resp = session.get(url, headers=header, params=params)
                                resp.encoding = "utf-8"
                                data = json.loads(resp.text)
                                if data["found"] == 0:
                                    continue
                                for vacancy in get_and_save_by_params(
                                    url, params=params
                                ):
                                    yield vacancy
