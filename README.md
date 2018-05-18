# Falcon REST API Starter Application

A **bare bones starter application** for a REST API backend based on 
[Falcon](http://falcon.readthedocs.io/en/stable/index.html) and a set 
of reasonable assumptions.

* [PostgreSQL](https://www.postgresql.org/) for database
* [SQLAlchemy](http://www.sqlalchemy.org/) ORM with [Psycopg2](http://initd.org/psycopg/)
* [Alembic](http://alembic.zzzcomputing.com/en/latest/) for database migration
* JSON Web Tokens for authorization (using the [PyJWT](https://pyjwt.readthedocs.io/en/latest/)
library)
* [Marshmallow](https://marshmallow.readthedocs.io/en/latest/index.html) for object serialization and validation.

This starter application was extracted from a current project and is 
intended to serve as scaffolding for similar REST API backends based on 
Falcon. The code works as part of the original application but has 
not been tested on its own so far. 

It provides only basic functionality:
* Database backend setup and database session management
* Secured resources (routes) using JSON Web Tokens
* Database migrations using Alembic

While I created this repository for my own use, anyone is welcome to 
use it for own purposes. If you find it useful please 
share your additions and improvements. I 
took a few shortcuts when I developed it, so there is much to improve.

Gelu @ [not-not.net](http://www.not-not.net) 