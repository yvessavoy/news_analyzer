from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserType:
    id: int = None
    type: str = None


@dataclass
class User:
    id: int = None
    last_name: str = None
    first_name: str = None
    type: int = None


@dataclass
class Article:
    id: int = None
    external_id: str = None
    author_last_name: str = None
    author_first_name: str = None
    site_name: str = None
    title: str = None
    length: int = 0
    published_at: datetime = None
    category: str = None
    comment_count: int = None
