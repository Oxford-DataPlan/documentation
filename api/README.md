# ODP API Documentation

This repository aims to serve as the documentation for using the ODP API. The swagger/docs page for the API will be available [here](https://api.uat.oxford-dp.link/api/docs)

# API testing with curl

#### Get the token
```
curl -X POST -H "Content-Type: application/json" -d '{
      "username": "",
      "password": ""
}' "https://oxford-dp.com/wp-json/jwt-auth/v1/token"
```
#### Expected Response
```
{
    "token": "<token>",
    "user_email": "user@example.com",
    "user_nicename": "user_display_name",
    "user_display_name": "User Name"
}
```
#### Call the api endpoint
##### /indexes endpoint (daily indices)
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "type": "daily",
      "duration_start": "2023-06-13",
      "duration_end": "2023-06-15",
      "company": "Meta"

}' "https://api.uat.oxford-dp.link/api/indexes"
```
##### Expected response daily indices
```
{
    "rows": [
        {
            "company_name": "Meta",
            "country": "",
            "date": "2023-06-13",
            "metric": "Ad Revenue",
            "value": 371126477.0
        },
        {
            "company_name": "Meta",
            "country": "",
            "date": "2023-06-14",
            "metric": "Ad Revenue",
            "value": 404982641.0
        },
        {
            "company_name": "Meta",
            "country": "",
            "date": "2023-06-15",
            "metric": "Ad Revenue",
            "value": 380078023.0
        }
    ]
}
```
##### /monthly_indices endpoint (monthly indices)
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "type": "daily",
      "duration_start": "2023-01-01",
      "duration_end": "2023-03-31",
      "company": "MFE"

}' "https://api.uat.oxford-dp.link/api/monthly_indices"
```
##### Expected response monthly indices
```
{
  "rows": [
    {
      "start_date": "2023-01-01",
      "end_date": "2023-01-31",
      "publication_date": "2024-02-07",
      "company_name": "MFE",
      "country": "IT",
      "metric": "Advertising Revenue",
      "value": 109767434.65438858,
      "category": "estimate"
    },
    {
      "start_date": "2023-02-01",
      "end_date": "2023-02-28",
      "publication_date": "2024-02-07",
      "company_name": "MFE",
      "country": "IT",
      "metric": "Advertising Revenue",
      "value": 108220551.8988177,
      "category": "estimate"
    },
    {
      "start_date": "2023-03-01",
      "end_date": "2023-03-31",
      "publication_date": "2024-02-07",
      "company_name": "MFE",
      "country": "IT",
      "metric": "Advertising Revenue",
      "value": 171890675.42930394,
      "category": "estimate"
    }
  ]
}
```
##### /outlook endpoint (outlook)
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "type": "daily",
      "duration_start": "2023-06-13",
      "duration_end": "2023-06-15",
      "company": "Fluidra"

}' "https://api.uat.oxford-dp.link/api/outlook"
```

##### Expected response outlook
```
{
    "rows": [
        {
            "company_name": "Fluidra",
            "country": "US",
            "date": "2023-06-13",
            "freq": "M",
            "metric": "Development Trends",
            "period": 6,
            "value": 4.0,
            "year": 2023
        },
        {
            "company_name": "Fluidra",
            "country": "US",
            "date": "2023-06-14",
            "freq": "M",
            "metric": "Development Trends",
            "period": 6,
            "value": 4.0,
            "year": 2023
        },
        {
            "company_name": "Fluidra",
            "country": "US",
            "date": "2023-06-15",
            "freq": "M",
            "metric": "Development Trends",
            "period": 6,
            "value": 4.0,
            "year": 2023
        }
    ]
}
```

# API testing with python

## Requirements
To test the service, export your ODP website email and password to the current shell and install the required libraries by running the following commands:

#### Exporting credentials
```setup
export ODP_WP_USER=""
export ODP_WP_PASSWORD=""
```
#### Installing libraries
```
pip install -r requirements.txt
```
OR

```
pip install pyjwt requests
```

## Test Cases
#### Example Test Case
##### /indexes endpoint
```
"TEST_CASE1": {
      "endpoint": "/indexes",
      "payload": {
          "type": "daily",
          "duration_start": "2024-06-08",
          "duration_end": "2024-06-15",
          "company": "Meta"
      },
      "headers": {
          "accept": "application/json",
          "Content-Type": "application/json"
      }
}
```

##### /monthly_indices endpoint
```
"TEST_CASE2": {
    "endpoint": "/monthly_indexes",
    "payload": {
        "type": "monthly",
        "duration_start": "2023-01-01",
        "duration_end": "2023-03-31",
        "company": "MFE"
    },
    "headers": {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
}
```

##### /outlook endpoint
```
"TEST_CASE3": {
    "endpoint": "/outlook",
    "payload": {
        "type": "daily",
        "duration_start": "2023-06-13",
        "duration_end": "2023-06-15",
        "company": "Fluidra"
    },
    "headers": {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
}
```
## Adding Test Cases
Either add companies in the `company_names` variable and select the test cases for the desired endpoint by choosing among `TEST_CASES_DAILY_INDICES`, `TEST_CASES_MONTHLY_INDICES` and `TEST_CASES_OUTLOOK`
or create your own test cases using the respective templates.

## Running the API
Finally, test the API using the following command
```
python test_api.py
```
## Response
If the username/email is incorrect, the response should be
```
status_code: 403
response: The provided password is an invalid application password.
```

If the password is incorrect, the response should be
```
status_code: 403
response: The provided password is an invalid application password.
```

If both username and password are correct, 
but the `type` is anything other than `daily`
the response should be
```
status_code: 400
{
  "detail": "type has to be 'daily'"
}
```

If both username and password are correct, 
but the `duration_start` is not in the format `YYYY-MM-DD` the response should be
```
status_code: 400
{
  "detail": "duration_start should be in the format YYYY-MM-DD"
}
```

If both username and password are correct, 
but the `duration_end` is not in the format `YYYY-MM-DD` the response should be
```
status_code: 400
{
  "detail": "duration_start should be in the format YYYY-MM-DD"
}
```

If both username and password are correct, 
but the `company` is empty the response should be
```
status_code: 400
{
  "detail": "company should not be empty"
}
```

If both username and password are correct, and the parameters are in the expected format, the response should be the requested json for [daily indices](#expected-response-daily-indices), [monthly indices](#expected-response-monthly-indices) and [outlook](#expected-response-outlook)