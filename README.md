# -QuadSciTest

QuadSci.ai technical interview/test

_How to run?_

- First run:

* sudo apt update
* sudo apt install python3 python3-pip python3-venv

or

- sudo apt update
- sudo apt install python3
- sudo apt install python3-pip
- sudo apt install python3-venv

* Then create the virtual environment:

- python3 -m venv venv

(the second venv is the name of the environment)

- Active the environment:

* source venv/bin/activate

---

- IMPORTANT \*

- The next two steps are performed at the level of the Windows or Unix folder depending on the operating system: \*

- Installation of dependencies \*

* Then, you can run for windows as administrator:

- install_dependencies.bat

* For Linux/Mac devices run:

- chmod +x install_dependencies.sh

* And then:

- install_dependencies.sh

Also you can install dependencies manually

- Installation of dependencies manually\*

- Install Flask and Taipy:

* pip install Flask taipy

- Run to install more dependencies

* pip install flask sqlalchemy psycopg2-binary apscheduler python-dotenv

* pip install psycopg2-binary

---

- DataBase installation: \*

- For the database dependencies you need to run for Linux:

* sudo apt install postgresql postgresql-contrib

- And then:

* sudo systemctl start postgresql

- For Windows you need to install PostgreSQL and start it.

---

- Start application \*

* For windows run as administrator:

- setup_databse.sh

* For linux or mac run:

- chmod +x setup_database.sh

* And then:

- setup_databse.sh

- Then check the database:

* sql -h localhost -U postgres -d postgres
* or psql -h localhost -U QuadSciTest -d SpaceX

http://127.0.0.1:5001/api/launches-clear
http://127.0.0.1:5001/api/starlink-clear
http://127.0.0.1:5001/api/rockets-clear

or

http://127.0.0.1:5001/api/launches-clear/json
http://127.0.0.1:5001/api/starlink-clear/json
http://127.0.0.1:5001/api/rockets-clear/json

- Finally run:

* app.py
