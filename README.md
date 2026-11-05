# Blog API

The Django REST backend for a small blogging platform. The React client is not
in this repository; it talks to these endpoints and sends the signed-in user's
id in the `X-User-Id` header.

## Apps

- `accounts`: header authentication, the current user and their posts
- `posts`: categories and posts
- `comments`: comment threads and replies on posts

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/api/me/` | the signed-in user |
| GET | `/api/me/posts/` | My Posts: every post the signed-in user wrote, drafts included |
| GET | `/api/categories/` | all categories |
| GET, POST | `/api/posts/` | the public feed; create a post |
| GET, PATCH, DELETE | `/api/posts/<id>/` | one post; only its author can change it |
| GET, POST | `/api/posts/<id>/comments/` | a post's comment thread; add a comment or a reply |

Creating a post needs `title`, `content` and `category` (a category slug).
`summary`, `tags` and `status` are optional; a new post is a draft unless
`status` is `published`.

## Running it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Tests

```bash
pytest
```
