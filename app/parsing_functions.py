from time import sleep
import requests
import fake_useragent
import json
from random import random, choice
from config import *
from proxy_list import proxy_list

session = requests.Session()
user = fake_useragent.UserAgent().random
header = {"user_agent": user}


def set_proxy(i=0, j=-1):
    global session
    proxy = choice(proxy_list[i:j])
    print(f"{proxy} - proxylist")
    session.proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    resp = session.get("https://httpbin.org/ip")
    print(resp.text)


def parse_developers():
    params = {"area": 1, "professional_role": 96}
    for industry in [7.538, 7.539, 7.540, 7.541]:
        params["industry"] = industry
        for exp in EXPERIENCE:
            for exp in EXPERIENCE:
                # print(
                #     f"industry_id = {industry},\
                #     experience = {exp}"
                # )
                params["experience"] = exp
                resp = session.get(API_URL, headers=header, params=params)
                resp.encoding = "utf-8"
                data = json.loads(resp.text)
                print(f"Found {data['found']} vacancies for ", params)
                if data["found"] == 0:
                    continue
                for vacancy in get_and_save_by_params(API_URL, params=params):
                    yield vacancy


def get_and_save_by_params(url, params):
    resp = session.get(url, headers=header, params=params)
    resp.encoding = "utf-8"
    data = json.loads(resp.text)
    if not data.get("pages") or not data.get("items"):
        print("========================================")
        print(data.keys())
        print("========================================")
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
                if archived is False:
                    archived = None
            except:
                archived = None
            try:
                schedule = vacancy["schedule"]["name"]
            except:
                schedule = None

            vacancy_url = vacancy["alternate_url"]
            vacancy_id = vacancy_url.split("/")[-1]

            vacancy_dict = {
                "vacancy_id": vacancy_id,
                "vacancy_name": vacancy_name,
                "profession": PROFESSIONAL_ROLES_ALL[params["professional_role"]],
                "industry": INDUSTRIES[params["industry"]],
                "experience": params["experience"],
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
                "employment_type": schedule,
                "vacancy_url": vacancy_url,
            }
            yield vacancy_dict


def parse_all(url, latest_only=False, start_area=None, end_area=None, i=0, j=-1):
    set_proxy(i, j)

    target_areas = AREA_IDS
    if start_area:
        target_areas = target_areas[start_area:]
    if end_area:
        target_areas = target_areas[:end_area]
    print(f"target areas: {target_areas[0]} ... {target_areas[-1]}")
    for area in target_areas:

        params = dict()
        if latest_only:
            params["search_period"] = 1
        sleep(random() * 5)
        params["area"] = area
        try:
            resp = session.get(url, headers=header, params=params)
            assert resp.status_code == 200
        except:
            set_proxy(i, j)
            resp = session.get(url, headers=header, params=params)
            assert resp.status_code == 200
        resp.encoding = "utf-8"
        data = json.loads(resp.text)
        # print(data.keys())
        # print(f"area={area}, found={data['found']}")
        print(f"Found {data['found']} vacancies for ", params)
        if data["found"] == 0:
            continue
        else:
            for professional_role_id in PROFESSIONAL_ROLES_ALL.keys():
                #
                # REMOVE
                #
                if area == 2 and professional_role_id < 8:
                    continue
                #
                # REMOVE
                #
                sleep(random() * 5)
                params["professional_role"] = professional_role_id
                if params.get("industry"):
                    params.pop("industry")
                if params.get("experience"):
                    params.pop("experience")
                try:
                    resp = session.get(url, headers=header, params=params)
                    assert resp.status_code == 200
                except:
                    set_proxy(i, j)
                    resp = session.get(url, headers=header, params=params)
                    assert resp.status_code == 200
                resp.encoding = "utf-8"
                data = json.loads(resp.text)
                print(f"Found {data['found']} vacancies for ", params)
                if data["found"] == 0:
                    continue
                else:
                    for industry_id in INDUSTRIES.keys():
                        sleep(random() * 5)
                        if (
                            area == 1
                            and professional_role_id == 96
                            and industry_id == 7
                            and not latest_only
                        ):
                            continue
                        # print(
                        #     f"area={area}, profession_id = {professional_role_id}, industry_id = {industry_id}"
                        # )
                        params["industry"] = industry_id
                        if params.get("experience"):
                            params.pop("experience")
                        try:
                            resp = session.get(url, headers=header, params=params)
                            assert resp.status_code == 200
                        except:
                            set_proxy(i, j)
                            resp = session.get(url, headers=header, params=params)
                            assert resp.status_code == 200
                        resp.encoding = "utf-8"
                        data = json.loads(resp.text)
                        print(f"Found {data['found']} vacancies for ", params)
                        if data["found"] == 0:
                            continue
                        else:
                            for exp in EXPERIENCE:
                                sleep(random() * 5)
                                # print(
                                #     f"area={area}, profession_id = {professional_role_id}, industry_id = {industry_id}, experience = {exp}"
                                # )
                                params["experience"] = exp
                                try:
                                    resp = session.get(
                                        url, headers=header, params=params
                                    )
                                    assert resp.status_code == 200
                                except:
                                    set_proxy(i, j)
                                    resp = session.get(
                                        url, headers=header, params=params
                                    )
                                    assert resp.status_code == 200
                                resp.encoding = "utf-8"
                                data = json.loads(resp.text)
                                print(f"Found {data['found']} vacancies for ", params)
                                if data["found"] == 0:
                                    continue
                                for vacancy_dict in get_and_save_by_params(
                                    url, params=params
                                ):
                                    yield vacancy_dict
