# Cook Book Project

This is a custom recipe storage site made so my family can store and share recipies we have gathered overtime.

## Features

- Account Creation
- Recipe Creation
- Faviorite recipies
- Ingredient Search

## Tech Stack

**Client:** Jinja

**Server:** Python, Flask

**Database** PostgresSQL

## Run Locally

Clone the project

```bash
  git clone https://github.com/shaunnnorton/Cook-Book-Project.git
```

Go to the project directory

```bash
  cd Cook-Book-Project
```

create .env

```bash
  echo "DATABASE_URL=sqlite:///database.db" > .env
  echo "SECRET_KEY=YOURKEYHERE" > .env
```

Install dependencies

```bash
  pip3 install requirements.txt
```

Start the server

```bash
  python3 app.py
```

## Running Tests

To run tests, run the following command

```bash
  python3 -m unitttest discover
```

## Authors

- [@shaunnnorton](https://www.github.com/shaunnnorton)

## Feedback

If you have any feedback, please reach out to me at shaunnorton@snorton.dev
