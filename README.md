# Micro blog "Blogicum", completed during training at [Yandex Prakticum](https://practicum.yandex.ru/)

## Desicription
Micro blog. Users can register, create posts, comment post of other users.

## Stack:
* Django templates
* Django ORM
* Django forms

### How to run the project:
Clone repository and go to it with the terminal:

```
git clone https://github.com/beluza-n/blogicum.git
```

```
cd blogicum
```

Create and activate virtual environment:

```
python3 -m venv venv
```

```
source venv/bin/activate
source venv/Scripts/activate (for Windows)
```

Update pip (optional):

```
python3 -m pip install --upgrade pip
```

Install dependencies from the requirements.txt:

```
pip install -r requirements.txt
```

Run migrations:

```
python3 manage.py migrate
```

Launch the Django project:

```
python3 manage.py runserver
```
:point_right: Note: on Windows use "python" command instead of "python3".