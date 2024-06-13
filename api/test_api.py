import os
import requests
import json
import jwt


def get_decoded_token(token):
    decoded_token = jwt.decode(
        token,
        algorithms=["HS256"],
        options=dict(verify_signature=False)
    )
    return decoded_token


if __name__ == "__main__":
    """
    Sometimes it's not possible to get the credentials from the environment variables,
    so we can provide them in a credentials.json file, or we can directly set their values here.
    """
    credentials_json_path = "credentials.json"
    if os.path.exists(credentials_json_path):
        with open(credentials_json_path, "r", encoding="utf-8") as f:
            credentials = json.loads(f.read())
        USER = {
            "username": credentials["ODP_WP_USER"],
            "password": credentials["ODP_WP_PASSWORD"]
        }
    else:
        USER = {
            "username": "" or os.getenv("ODP_WP_USER"),
            "password": "" or os.getenv("ODP_WP_PASSWORD")
        }


    AUTH_URL = "https://oxford-dp.com/wp-json/jwt-auth/v1/token"
    API_URL = "https://api.uat.oxford-dp.link/api"

    auth_response = requests.post(
        AUTH_URL,
        data=USER
    )
    auth_response_json = auth_response.json()
    if auth_response.status_code != 200:
        print(f"status_code: {auth_response_json['data']['status']}")
        print(f"response: {auth_response_json['message']}")
        exit()

    token = auth_response_json.get("token")


    company_names_allowed = get_decoded_token(token)['roles'].split(",")

    company_names = [
        "Deliveroo",
        "Meta",
        'Asos'
    ]

    company_names = company_names_allowed

    TEST_CASES_DAILY_INDICES = {
        f"TEST_CASE{i}": {
            "endpoint": "/indexes",
            "payload": {
                "type": "daily",
                "duration_start": "2023-06-08",
                "duration_end": "2023-06-15",
                "company": test_company
            },
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        } for i, test_company in enumerate(company_names)
    }

    TEST_CASES_MONTHLY_INDICES = {
        f"TEST_CASE{i}": {
            "endpoint": "/monthly_indexes",
            "payload": {
                "type": "monthly",
                "duration_start": "2021-06-08",
                "duration_end": "2023-06-15",
                "company": test_company
            },
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        } for i, test_company in enumerate(company_names)
    }

    TEST_CASES_OUTLOOK = {
        f"TEST_CASE{i}": {
            "endpoint": "/outlook",
            "payload": {
                "type": "daily",
                "duration_start": "2023-06-08",
                "duration_end": "2024-06-15",
                "company": test_company
            },
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        } for i, test_company in enumerate(company_names)
    }

    TEST_CASES = TEST_CASES_DAILY_INDICES
    # TEST_CASES = TEST_CASES_MONTHLY_INDICES
    # TEST_CASES = TEST_CASES_OUTLOOK


    for key, value in TEST_CASES.items():
        print(f"--- Running test {key} ---")
        payload = value.get('payload')
        headers = value.get('headers', {})
        headers.update({"Authorization": f"Bearer {token}"})
        endpoint = value.get('endpoint')
        print(f"{payload['company']}, {endpoint}")

        test_response = requests.post(
            f"{API_URL}{value.get('endpoint')}",
            json=payload,
            headers=headers
        )
        try:
            response_code = test_response.status_code
            if response_code == 200:
                print(f"status_code: {test_response.status_code}")
                print(json.dumps(test_response.json(), indent=2))
            else:
                print(f"status_code: {test_response.status_code}")
                print(test_response.text)
        except Exception as e:
            print(f"Error: {e}")
