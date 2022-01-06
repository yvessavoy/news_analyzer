# News Analyzer
This project aims to gather information about what, how and by whom content is published on swiss news sites.
It also shows an overview of the amount of articles published in a specific category, by a specific author or
on a specific day.

## Setup
The following environment variables are needed to run news analyzer:
- export PYTHONPATH=$PYTHONPATH:/path/to/the/application
- DB_USER: MySQL Username
- DB_PASSWORD: MySQL Password

## Available Scripts
### General
- Setup database: `poetry run python news_analyzer/setup_db.py <user> <password>`

### Readers
- 20min.ch: `poetry run python news_analyzer/readers/20min.py`
- tagesanzeiger.ch: `poetry run python news_analyzer/readers/tagesanzeiger.py`
- blick.ch: `poetry run python news_analyzer/readers/blick.py`

### Visualize Data
`poetry run python news_analyzer/visualize.py`

## Database Design
### Site
| ID | Name     |
|----|----------|
| 1  | 20min    |
| 2  | Blick    |

### Category
| ID | Name     |
|----|----------|
| 1  | Sport    |
| 2  | Schweiz  |
| 3  | Ausland  |

### Author
| ID | Last Name | First Name |
|----|-----------|------------|
| 1  | Mueller   | Max        |
| 2  | Heiri     | Hans       |

### Article
| ID | Article ID | Author ID | Site ID | Title                  | Article Length | Comment Count | Published at        | Category ID | 
|----|------------|-----------|---------|------------------------|----------------|---------------|---------------------|-------------|
| 1  | 123456789  | 1         | 1       | Corona-Zahlen fallen   | 3132           | 645           | 2021-10-27-16:13:05 | 2           |
| 2  | 778899112  | 2         | 2       | Schweiz gewinnt die WM | 1322           | 1670          | 2021-10-28-22:35:13 | 1           |
