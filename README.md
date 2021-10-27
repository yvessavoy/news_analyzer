# News Analyzer
This project aims to gather information about what, how and by whom content is published on swiss news sites.
It also shows an overview of the amount of articles published in a specific category, by a specific author or
on a specific day.

## Setup
The following environment variables are needed to run news analyzer:
- export PYTHONPATH=$PYTHONPATH:/path/to/the/application
- DB_USER: MySQL Username
- DB_PASSWORD: MySQL Password

## Database Design
### Site
| ID | Sitename |
|----|----------|
| 1  | 20min    |
| 2  | Blick    |

### Author
| ID | Name    | First Name |
|----|---------|------------|
| 1  | Mueller | Max        |
| 2  | Heiri   | Hans       |

### Article
| ID | Site ID | Title | Length | Published at | Author ID | Has Comments | Comment Count |
|----|---------|-------|--------|--------------|-----------|--------------|---------------|