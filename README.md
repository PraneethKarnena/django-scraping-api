## Django - Asynchronous Web Scraping

A simple Django project to demonstrate the scraping of a website asynchronously.

**Demo:** [https://django-async-web-scraping.herokuapp.com/](https://django-async-web-scraping.herokuapp.com/)

**Tools**:

 - Django
 - Django Rest Framework
 - Heroku

**How this works:**

 - User makes a `POST` request to the API.
 - Sends a list of `URLs` and an `Email ID` as payload
 - The system will then download each `URL` along with static assets and HTML files, asynchronously
 - Compresses the downloaded files and sends an email to the address in the payload

**Routes:**

- Base URL: `https://django-async-web-scraping.herokuapp.com/api/v1/`
- Scrape Request: `https://django-async-web-scraping.herokuapp.com/api/v1/scrape/`
- Request Method: `POST`
- Scheme:
```json
{
"urls": [
"https:/www.google.co.in/",
"https://www.apple.com/"
],
"email": "user@example.com"
}
```
