# Combined Database Labs 2 and 3

**Student Name:** Mariam Ahmed Mohamed
**Student ID:** 2304242

## 1. Project Overview

This repository contains the combined submission for Database Labs 2 and 3. It includes SQL scripts for the required database tasks and a Flask-based website that integrates user authentication, a personal To-Do list, and a Library Management System.

The project demonstrates relational database design, SQL DDL and DML operations, primary and foreign key constraints, and the integration of a web application with a MySQL database.

## 2. Repository Structure

```text
lab3-2304242/
├── .gitignore
├── .htaccess
├── README.md
├── problem1_DDL.sql
├── problem1_DML.sql
├── problem1_Answers.txt
├── problem2_DDL.sql
├── problem2_DML.sql
└── website/
    ├── .gitignore
    ├── app.py
    ├── requirements.txt
    ├── settings.env          # Local configuration; not committed
    ├── static/
    │   ├── images/
    │   ├── library_style.css
    │   └── validate.js
    └── templates/
        ├── author_form.html
        ├── base.html
        ├── book_form.html
        ├── error.html
        ├── library.html
        ├── login.html
        ├── register.html
        └── todos.html
```

**Note:** `website/settings.env` is a local configuration file and is intentionally excluded from the public repository. Create it locally before running the application.

## 3. Technologies Used

- **Python** — application logic.
- **Flask** — web framework.
- **MySQL** — relational database management system.
- **PyMySQL** — Python–MySQL connectivity.
- **HTML and CSS** — page structure and styling.
- **JavaScript** — client-side validation.
- **Git and GitHub** — version control and source-code hosting.

## 4. SQL Assignment Files

The repository contains the following SQL files:

| File | Purpose |
|---|---|
| `problem1_DDL.sql` | Creates the tables and constraints required for Problem 1. |
| `problem1_DML.sql` | Inserts and manipulates data for Problem 1. |
| `problem1_Answers.txt` | Contains the answers and explanations for Problem 1. |
| `problem2_DDL.sql` | Creates the Library database tables and relationships. |
| `problem2_DML.sql` | Inserts the sample data required for Problem 2. |

### Problem 1: Company Database

This part covers the `EMPLOYEE`, `DEPARTMENT`, and `PROJECT` tables, their relationships, and the required data-definition and data-manipulation operations.

The file `problem1_Answers.txt` documents the answers to Questions Q1.1–Q1.3, including relevant execution results, database errors, and the explanation of the circular dependency.

### Problem 2: Library Database

This part implements the database structure for books and authors.

The intended relationship is that each book references an author through `BOOK.author_id`, which references `AUTHOR.author_id`.

The database design includes primary keys and a foreign key relationship. The author deletion constraint is configured to cascade deletion to related books, as required by the assignment.

The DML script provides sample author and book records.

## 5. Website Features

The Flask website includes the following pages and functionality:

- **User Registration and Login:** Provides user registration and login pages.
- **Personal To-Do List:** Allows users to access and manage their tasks.
- **Library Management:** Displays the library collection and provides book-management forms.
- **Author Management:** Provides forms for managing author records.
- **Book Management:** Includes forms for adding and editing book details, including the title, price, and associated author.
- **Visual Design:** Uses CSS styling and local image assets to improve the website's appearance.
- **Form Validation:** Uses HTML validation and JavaScript where implemented.

The availability of each individual operation depends on the application's current implementation and database configuration. See the testing section below for the functionality observed during local testing.

## 6. Database Relationships

The project uses relational tables and key constraints to maintain relationships between records.

- **To-Do System:** The `todos.user_id` column references `users.user_id`, associating tasks with their users.
- **Library System:** The `BOOK.author_id` column references `AUTHOR.author_id`, associating books with authors.
- **Company Database:** Problem 1 defines the relationships among the `EMPLOYEE`, `DEPARTMENT`, and `PROJECT` tables according to the assignment requirements.

The SQL scripts should be executed in the same database and in the order described in the setup instructions.

## 7. Requirements

Before running the project, ensure that the following are available:

- Python 3.10 or later.
- MySQL Server.
- MySQL credentials with permission to create and modify the project database.
- Internet access when installing Python packages, unless the packages are already available locally.
- MySQL Workbench or another MySQL client for executing the SQL scripts.

## 8. Installation and Setup

### Step 1: Clone or Download the Repository

Clone the repository:

```bash
git clone https://github.com/mariam-ahmed2006/lab3-2304242.git
cd lab3-2304242
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 2: Create the Database

Open MySQL Workbench or another MySQL client and execute:

```sql
CREATE DATABASE IF NOT EXISTS combined_labs;
USE combined_labs;
```

### Step 3: Execute the SQL Scripts

Execute the following files in order, using the same MySQL connection and the `combined_labs` database:

1. `problem1_DDL.sql`
2. `problem1_DML.sql`
3. `problem2_DDL.sql`
4. `problem2_DML.sql`

Check each script for errors before proceeding to the next one.

**Important:** If the scripts contain their own `CREATE DATABASE`, `USE`, or table-reset statements, check those statements before execution. Running setup scripts repeatedly may recreate tables, remove existing data, or produce errors, depending on their contents.

### Step 4: Configure the Website

Create a local file named `settings.env` inside the `website/` directory.

Add the environment variables expected by `website/app.py`. For example, if the application uses the variable names below:

```dotenv
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=combined_labs
SECRET_KEY=replace_with_a_long_random_secret
```

Replace the example values with your actual MySQL credentials and a randomly generated Flask secret key.

**Important:** These variable names are examples. Before running the website, confirm that they match the names read by `website/app.py`. Do not upload real database passwords or secret keys to GitHub.

### Step 5: Install Python Dependencies

From the repository root, run:

```bash
python -m pip install -r website/requirements.txt
```

If your system uses a different Python launcher, use the Python command associated with your installed version.

### Step 6: Run the Flask Application

From the repository root, run:

```bash
python website/app.py
```

Open the local address shown in the terminal. The configured default address is:

```text
http://127.0.0.1:5001
```

If the application starts on a different port, use the address printed by Flask.

To register a new account, open:

```text
http://127.0.0.1:5001/register
```

## 9. Testing and Verification

The following behavior was observed during local testing:

- The Flask application started and served the tested pages.
- The registration, login, Library, and To-Do routes returned successful HTTP responses during the observed test session.
- Local image assets loaded successfully.
- A To-Do deletion request returned a redirect, followed by a successful response from the To-Do page.

These observations confirm that the tested pages and requests were accessible at that time. They do **not** independently confirm that every database operation works correctly.

Before submission, test the following operations against the configured MySQL database:

- Register an account and log in.
- Create, view, update, and delete To-Do items, where supported.
- Add a book and verify that it appears in the library.
- Edit a book and verify that the changes are saved.
- Delete a book and verify that it is removed.
- Add, edit, and delete authors, where supported.
- Verify the foreign key relationship between books and authors.
- Verify the required cascading behavior when deleting an author.
- Execute all four SQL scripts and confirm that their results match the assignment requirements.

Only mark an operation as tested after verifying its result.

## 10. Security and Configuration Notes

- The `website/settings.env` file is intended for local configuration and is excluded from version control.
- Database passwords and Flask secret keys should never be committed to the repository.
- The Flask development server is intended for local development and testing, not production deployment.
- The `.htaccess` file does not, by itself, run a Flask application; deployment depends on the server configuration.

## 11. GitHub Repository

Repository link:

https://github.com/mariam-ahmed2006/lab3-2304242



