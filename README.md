# Sentiment News Backend
A simple REST API for a financial news sentiment [app](https://sentiment-news.vercel.app/)

[Frontend Repo](https://github.com/Marvin-Deng/Sentiment-News)

## Backend Tech Stack
- Python
- FastAPI
- Tortoise-ORM
- PostgreSQL

## Installation

1. Clone the repo
```shell
git clone https://github.com/Marvin-Deng/Sentiment-News-Backend.git
```

2. Install requirements
```shell
pip install -r requirements.txt
```

3. Run locally using 
```shell
`hypercorn main:app --reload`
```

4. Run tests
```shell
nose2
```