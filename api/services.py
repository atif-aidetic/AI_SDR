import requests
import time
import json
import pandas as pd
from open_ai import OpenAI
from settings import ENV

env = ENV()

apollo_key = env.APOLLO_AUTH_KEY
openai_api_key = env.openai_api_key
apollo_company_search = env.apollo_company_search
apollo_people_search = env.apollo_people_search


def generate_keywords(query, openai_api_key):
    model = "gpt-3.5-turbo"
    max_tokens = 150
    api_key = openai_api_key
    client = OpenAI(api_key=api_key)

    prompt = f'Given the user query: "{query}", extract keywords that can be used to find relevant companies in a large dataset. These keywords will be used to match against company descriptions and locations.\n\n'
    prompt += "Please provide the following information in JSON format:\n"
    prompt += (
        '{ "industry_keywords": [], "location_keywords": [], "range_of_employees": []}'
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in keyword extraction for finding relevant companies. Your task is to extract keywords from the user query to locate businesses in a large dataset.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)


def fetch_organizations(task):
    url = apollo_company_search
    headers = {"Cache-Control": "no-cache", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=task)

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", 60)
        time.sleep(int(retry_after))
        response = requests.post(url, headers=headers, json=task)

    return response.json()


def fetch_leads(task):
    r = requests.post(apollo_people_search, json=task)

    if r.status_code == 429:
        retry_after = r.headers.get("Retry-After", 60)
        time.sleep(int(retry_after))
        r = requests.post(apollo_people_search, json=task)

    return r.json()


def getting_cxo_result(content):
    query = content["query"]
    positions = content["positions"]

    keywords = generate_keywords(query, openai_api_key)
    print("enter into the getting CXO")
    industries = keywords.get("industry_keywords", [])
    locations = keywords.get("location_keywords", [])
    employee_range = keywords.get("range_of_employees", [])

    task_org = {
        "api_key": apollo_key,
        "page": 1,
        "per_page": 100,
        "organization_num_employees_ranges": employee_range,
        "organization_locations": locations,
        "q_organization_keyword_tags": industries,
    }

    org_response = fetch_organizations(task_org)

    total_orgs = org_response.get("pagination", {}).get("total_entries", 0)
    total_pages = org_response.get("pagination", {}).get("total_pages", 1)

    organizations = []
    for account in org_response.get("accounts", []) + org_response.get(
        "organizations", []
    ):
        organization_data = {
            "name": account.get("name", "N/A"),
            "domain": account.get("website_url", "N/A"),
            "city": account.get("organization_city", "N/A"),
            "state": account.get("organization_state", "N/A"),
            "country": account.get("organization_country", "N/A"),
        }
        organizations.append(organization_data)

    leads = []
    if total_orgs > 0:
        org_domains = "\n".join(
            [
                org["domain"]
                for org in organizations
                if org["domain"] not in ("N/A", None)
            ]
        )

        cleaned_string = positions.strip("[]").strip("'")
        positions = cleaned_string.split(",")
        positions = [positions]
        task_lead = {
            "api_key": apollo_key,
            "q_organization_domains": org_domains,
            "page": 1,
            "per_page": 100,
            "person_titles": positions,
        }

    print("position", positions)
    ## changes to be done here
    lead_response = fetch_leads(task_lead)

    total_leads = lead_response.get("pagination", {}).get("total_entries", 0)
    total_lead_pages = lead_response.get("pagination", {}).get("total_pages", 1)

    for person in lead_response.get("people", []):
        lead_data = {
            "id": person.get("id", "N/A"),
            "name": person.get("name", "N/A"),
            "organization": person.get("organization", {}).get("name", "N/A"),
            "domain": person.get("organization", {}).get("primary_domain", "N/A"),
        }
        print(lead_data)
        leads.append(lead_data)

    extracted_details = []
    for i in lead_response["contacts"]:
        # Check if 'contact_emails' exists and has at least one element
        email = "N/A"
        if "contact_emails" in i and len(i["contact_emails"]) > 0:
            email = i["contact_emails"][0].get("email", "N/A")

        # Extract and store the required fields with default values
        extracted_details.append(
            {
                "company_name": i.get("organization", {}).get("name", "N/A"),
                "company_domain": i.get("organization", {}).get(
                    "primary_domain", "N/A"
                ),
                "name": i.get("name", "N/A"),
                "linkedin_url": i.get("linkedin_url", "N/A"),
                "title": i.get("title", "N/A"),
                "email": email,
            }
        )

    print(extracted_details[0])
    print(extracted_details[1])
