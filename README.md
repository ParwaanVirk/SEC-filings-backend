# SEC Filings Analyzer
SEC Filings analyzer

## Prerequisites
Install Node.js which includes Node Package Manager

## Installation

### Frontend

1. Clone this repository on local machine
```
git clone https://github.com/ashutoshc8101/sec-fillings-frontend.git
```

2. Install dependencies using npm
```
npm install
```

3. Run frontend locally using
```
npx ng serve
```

### Backend
Python >= 3.7 recommended. Python 2 not supported.

**Installation**

```
git clone https://github.com/ashutoshc8101/SEC-filings-backend.git
cd SEC-filings-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Scraping**:
```
cd scraping
python scrape.py
```

**Run backend server**:
```
python manage.py runserver
```

**Feeding companies to backend**
This process is manual for now but it is planned to be automated.
- Run django backend server using `python manage.py runserver`
- Visit http://localhost:8000/admin/ and login using the superuser credentails
- Once logged in, add companies with their CIK and ticket numbers.
![image](https://user-images.githubusercontent.com/24855641/159132813-d90c41cc-30fc-490d-a888-c35d13e6c85f.png)

**Seeding**:
Note, Feeding companies to backend is a pre-requisite for this step.

Database should be seeded from the csv files before actual usage of the application.
**Manual**:
This can be done by sending a GET request to route `/company/seeder/`.

**CRON Jobs**:
A cron job is set up for seeding the backend database from scraped csv filings.

Instructions for using cron jobs
```
python manage.py crontab add
```

## Problem Statement
The SEC’s EDGAR database contains terabytes of documents and data, including press releases,
annual corporate filings, executive employment agreements, and investment company
holdings. While EDGAR has existed for over twenty years, scholars have had difficulty
conducting or reproducing research based on EDGAR data. Researchers often spend a lot of
time and money developing and redeveloping code to retrieve and parse EDGAR data with no
common bottom-up framework.

## Functionalities
- Metrics of SaaS companies can be viewed on an interactive web dashboard.
  ![image](https://user-images.githubusercontent.com/24855641/159131695-d9fc4c3f-49dd-464a-8a18-3611c84eaa11.png)

- Side by side comparison of two companies.
  ![image](https://user-images.githubusercontent.com/24855641/159131713-fdf8c7d8-19a6-477f-b6a1-0ab353eb777e.png)
  ![image](https://user-images.githubusercontent.com/24855641/159131727-aad9de5a-af6c-4e54-a55a-0c5ed63f57fe.png)


- Rating of a company in terms of Profitability, Investability and Growth.
  ![image](https://user-images.githubusercontent.com/24855641/159119143-ef16b0c3-0d90-42f7-be31-c13ef8f3ce56.png)

- Most viewed SaaS companies are available on search page for easier access.
  ![image](https://user-images.githubusercontent.com/24855641/159119153-be9755ac-c1f2-43a2-a75e-6e799a920123.png)

- SaaS companies can be marked as favourites.
  ![image](https://user-images.githubusercontent.com/24855641/159119341-b6dbccbb-c100-4a36-9c8f-c94f4b952e3f.png)

## Architecture Overview:
![flow_diagram_digital_alpha (1)](https://user-images.githubusercontent.com/24855641/159120589-f75b97fa-774d-4a2e-b317-7cd86ee4836d.png)


- The source of metrics in our app is EDGAR. Edgar API is used to scrap metrics.
- The scrapped forms (10K, 10Q, 8K) are stored as csv files.
- A scheduled cron job reads these scrapped csv files, obtain neccessary metrics and seeds them into the backend database.
- The django backend reads the database and provides the necessary data to the frontend. It also powers user authentication, search and favourites functionalities.
- Frontend written using angular provides a fluid dashboard for easy viewing and comparision of SaaS metrics.

## ML Model Used:
Since we had a small training dataset, we went on to use simple machine learning regression models to fit our data. Experiments were performed with three different machine learning models, namely Ridge Regression, SVM Regressor and Lasso Regression. Among these the Lasso model which uses L1 regularization, yielded the best generalization for the validation dataset. 
Two different models were deployed with each category considered as a separate label in each dataset.
Growth estimation model.
Profitability estimation model
The lasso procedure encourages simple and sparse models(i.e models with fewer parameters). It also helps reduce overfitting of the model to the dataset, which had to be specially dealt with in this case. Thus the lasso model was chosen and the results have been displayed on the dashboard.


## Technologies Used:
- [Edgar API](https://www.sec.gov/edgar/sec-api-documentation)
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Django](https://www.djangoproject.com/)
- [Angular](https://angular.io/)
