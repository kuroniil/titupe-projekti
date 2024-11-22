# Running the application:
1. Run <code>python3 create_db.py</code> in the root directory
2. Run <code>python3 manage.py migrate</code>
3. Now you can start the app with <code>python3 manage.py runserver</code>

The python script will create the database with 2 premade users:
- **Username**: bob  - **Password**: passwd  _(Not admin)_
- **Username**: admin  - **Password**: coffee  _(Admin)_
