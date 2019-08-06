## Django - Asynchronous Web Scraping

A simple Django project to demonstrate the scraping of a website asynchronously. 

**Tools**:

 - Django
 - Django Rest Framework
 - Heroku
 - Celery

**How this works:**

 - User makes a `POST` request to the API. 
 - Sends a list of `URLs` and an `Email ID` as payload
 - The system will then download each `URL` along with static assets and HTML files, asynchronously
 - Compresses the downloaded files and sends an email to the address in the payload
