
The goal of this project is to experiments with kubernetes.
Python3.10, FastApi, Postgress, docker compose V2 are used.

**Prerequisite**

DB Postgress

**How to use with docker compose**

To start project
Build project:

<code>bash build.sh</code>

Run containers:

<code>docker compose up</code>

Create db tables

<code>docker compose exec backend alembic upgrade head</code>

And access it through the browser:

<code>http://127.0.0.1:8000/docs</code>


**How to use with kubernetes**
