# Combined Labs 2 and 3

Mariam Ahmed Mohamed — 2304242 

This is the existing Python/Flask website with login, personal to-dos, authors,
books, and images connected to ONE database: `combined_labs`.

## Files

- `website/app.py`: the website backend; Python was used in both original labs.
- `website/templates/` and `website/static/`: the original pages, styling, validation, and images.
- `website/requirements.txt`: the four Python libraries needed to run the site.
- `website/settings.env`: visible database connection and session settings.
- `problem1_DDL.sql`, `problem1_DML.sql`: company tables and sample data.
- `problem1_Answers.txt`: company foreign-key answers and observed errors.
- `problem2_DDL.sql`, `problem2_DML.sql`: login/to-do/library tables and library sample data.
- `.htaccess`: protects these Python source/configuration files from Apache access.

There are no virtual environments, cache folders, tests, screenshots,
or copies of the original projects in this delivery. The only setup helper is
`RUN_ME_FIRST.py`, which can be deleted after setup.

## Easiest way for her to run it on Windows

1. Extract the ENTIRE ZIP. Do not run files from inside the ZIP preview.
2. Open `RUN_ME_FIRST.py` in VS Code and press the same **Run Python File**
   button used for `app.py`. Double-clicking also works if Windows opens `.py`
   files with Python.
3. Wait while the libraries install. An internet connection is needed the first time.
4. A small window asks for the MySQL connection. Enter the password she uses in
   MySQL Workbench, then click **Set up and open website**. Host, port, and username
   normally stay at their defaults; change them if her Workbench connection differs.
5. The helper creates the database, imports all four SQL files, checks the seven
   tables and five foreign keys, saves the settings, starts Flask, and opens the browser.
   Register an account there. Keep the terminal window open while using the site.

Python 3.10+ and the MySQL server used by her Workbench connection must already
be installed and running. The helper installs Python libraries, including bcrypt
and MySQL password-authentication support, into the same Python that runs it.
It does not install the MySQL server, recover forgotten passwords, or delete databases.

After the site works, close its terminal or press Control+C to stop it. She can
then **delete `RUN_ME_FIRST.py` safely**. Keep `website/settings.env`: it stores
her saved connection and session settings. Next time, open `website/app.py` in
VS Code, press Run, and open the address printed in its terminal. No setup or
SQL import is needed again. The helper is not imported by the website.

If setup cannot finish, it prints the problem and waits for Enter, so she can
send a screenshot instead of the window disappearing. Never send the password.
If port 5001 is already in use, it chooses another free port and opens that address.

## Manual setup (only if not using the helper)

Start MySQL in XAMPP. On this Mac:

```bash
sudo /Applications/XAMPP/xamppfiles/xampp startmysql
```

Then paste these commands:

```bash
cd /Applications/XAMPP/xamppfiles/htdocs/Help/combined-labs
/Applications/XAMPP/xamppfiles/bin/mysql -h 127.0.0.1 -u root < problem1_DDL.sql
/Applications/XAMPP/xamppfiles/bin/mysql -h 127.0.0.1 -u root < problem1_DML.sql
/Applications/XAMPP/xamppfiles/bin/mysql -h 127.0.0.1 -u root < problem2_DDL.sql
/Applications/XAMPP/xamppfiles/bin/mysql -h 127.0.0.1 -u root < problem2_DML.sql
```

On another computer, execute those same four files in that order in MySQL
Workbench. Or use that computer's `mysql` command instead of the Mac path.
If the MySQL account has a password, add `-p` to each command and enter it in
`website/settings.env`. The supplied configuration is for local XAMPP with
username `root` and a blank password.

These scripts create seven tables and five foreign keys. They keep existing
rows on re-run. There are three authors, six books, three departments, three
employees, and three projects. Create your own user account through the site.

## Start the website

In a terminal inside `website/`:

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

On Windows, use `python` in place of `python3`.

Open **http://127.0.0.1:5001/register**. Register, then switch between **My to-dos**
and **Library** using the navigation. Press **Control+C** to stop Flask.
Apache does not run Python/Flask; XAMPP supplies MySQL, and Flask runs the site
at the address above. Python 3.10+ is required. Library pages require login;
the catalog is shared, while each user's tasks remain private.

## How the labs are connected

`get_db()` in `website/app.py` reads `website/settings.env` for every section.
Both labs now use `combined_labs`, rather than separate `registration`,
`library`, and `company` databases. This intentionally changes the handouts'
separate database names to provide the requested single database.

- `todos.user_id` references `users.user_id`.
- `BOOK.author_id` references `AUTHOR.author_id`; deleting an author deletes their books.
- Employees and projects reference departments; a department's manager references an employee.
- Company tables are the SQL exercise; the handout does not require company web pages.

The seven tables do not all need foreign keys to one another to share one
database. To-dos do not need a book ID, for example.

The working integration passed 13 real-MySQL tests, and its pages were checked
at desktop and 360 px phone widths before the development files were removed.
This is a local lab application. Keep connection settings private and change
the session key if sharing or publishing a real installation.
