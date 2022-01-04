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
class Site:
    id: int = None
    name: str = None


@dataclass
class Category:
    id: int = None
    name: str = None


@dataclass
class Article:
    id: int = None
    external_id: str = None
    author_id: int = None
    site_id: int = None
    title: str = None
    length: int = 0
    published_at: datetime = None
    category_id: int = None


@dataclass
class Comment:
    id: int = None
    article_id: int = None
    user_id: int = None
    submitted_at: datetime = None
