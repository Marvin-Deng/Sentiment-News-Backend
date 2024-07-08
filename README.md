# Sentiment News Backend

A simple REST API for a financial news sentiment [app](https://sentiment-news.vercel.app/) with Gemini for sentiment analysis. 

[Frontend Repo](https://github.com/Marvin-Deng/Sentiment-News)

## Backend Tech Stack

- Python
- FastAPI
- Tortoise-ORM
- PostgreSQL

## Setup

1. Clone the repo

```shell
git clone https://github.com/Marvin-Deng/Sentiment-News-Backend.git
```

2. Create virtual environemnt

```shell
python3 -m venv venv

# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate
```

3. Install requirements

```shell
pip install -r requirements.txt
```

4. Get free API keys and fill in values in `.env`

- [RapidAPI](https://rapidapi.com/hub)
- [Finnhub](https://finnhub.io/)
- [Tinngo](https://www.tiingo.com/)
- [Gemini](https://ai.google.dev/)
- [Postgres](https://supabase.com/)

## Running

```shell
hypercorn src/main:app --reload
```

## Formatting

```shell
black .
```

## Testing

```shell
pytest
```

## Updating requirements

```shell
pip freeze > requirements.txt
```