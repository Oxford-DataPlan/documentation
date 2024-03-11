# ODP API Documentation

This repository aims to serve as the documentation for using the ODP API. The swagger/docs page for the API will be available [here](https://api.uat.oxford-dp.link/api/docs)

# API testing with curl

#### Get the token
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "", "password": ""}' "https://oxford-dp.com/wp-json/jwt-auth/v1/token"
```
#### Expected Response
```
{"token":"<token>","user_email":"user.name@example.com","user_nicename":"user-name-example-com","user_display_name":"User Name"}
```
#### Call the api endpoint
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "type": "daily",
      "duration_start": "2020-06-08",
      "duration_end": "2023-06-15",
      "company": "Meta"

}' "https://api.uat.oxford-dp.link/api/indexes"
```
#### Expected Response
```
{
  "rows": [
    {
      "company_name": "company",
      "country": "country",
      "date": "2023-06-21",
      "metric": "metric1",
      "value": 123.456
    },
    {
      "company_name": "company",
      "country": "country",
      "date": "2023-06-20",
      "metric": "metric2",
      "value": 789.123
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
pyjwt
requests

```

## Test Cases
#### Example Test Case
```
"TEST_CASE1": {
    "endpoint": "/indexes",
    "payload": {
        "type": "daily",
        "duration_start": "2023-06-08",
        "duration_end": "2023-06-15",
        "company": "Xing"
    },
    "headers": {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
}
```
## Adding Test Cases
Simply add a new entry in the `TEST_CASES` dictionary in `api_test_cases.py`, and update the `type`, `duration_start`, `duration_end` and `company` accordingly

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

If both username and password are correct, and the parameters are in the expected format, the response should be the requested json
```
status_code: 200
{
  "rows": [
    {
      "company_name": "company",
      "country": "country",
      "date": "2023-06-21",
      "metric": "metric1",
      "value": 123.456
    },
    {
      "company_name": "company",
      "country": "country",
      "date": "2023-06-20",
      "metric": "metric2",
      "value": 789.123
    }
  ]
}
```