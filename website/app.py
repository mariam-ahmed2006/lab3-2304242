
import os
import pymysql
import bcrypt
import uuid
import secrets
from pathlib import Path

from decimal import Decimal, InvalidOperation
from flask import Flask, render_template, request, redirect, session, url_for, flash, abort
from dotenv import load_dotenv
from werkzeug.utils import secure_filename


load_dotenv(Path(__file__).with_name("settings.env"), interpolate=False)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Missing SECRET_KEY. Check website/settings.env.")
app.config.update(MAX_CONTENT_LENGTH=8 * 1024 * 1024, SESSION_COOKIE_SAMESITE="Lax")


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "combined_labs"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.before_request
def protect_private_pages():
    public_endpoints = {"index", "register", "login", "static"}
    if request.endpoint and request.endpoint not in public_endpoints and "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        expected = session.get("csrf_token", "")
        supplied = request.form.get("csrf_token", "")
        if not expected or not secrets.compare_digest(expected.encode("utf-8"), supplied.encode("utf-8")):
            abort(400, description="Your form expired. Reload the page and try again.")


@app.context_processor
def form_security():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return {"csrf_token": session["csrf_token"]}


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


def save_uploaded_image(field_name):
    image = request.files.get(field_name)

    if not image or image.filename == "":
        return None

    original_name = secure_filename(image.filename)

    if "." not in original_name:
        raise ValueError("Please upload a valid image file.")

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only JPG, JPEG, PNG, WEBP, and GIF images are allowed."
        )

    image_folder = os.path.join(
        app.root_path, "static", "images"
    )
    os.makedirs(image_folder, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.{extension}"
    image_path = os.path.join(image_folder, filename)

    image.save(image_path)

    return f"images/{filename}"


@app.route("/")
def index():
    return redirect(url_for("todos" if "user_id" in session else "login"))

@app.route("/library")
def library_index():
    db = get_db()

    try:
        with db.cursor() as cursor:
            # Get all books with their author names
            cursor.execute("""
                SELECT
                    BOOK.book_id,
                    BOOK.image_url,
                    BOOK.title,
                    BOOK.price,
                    BOOK.author_id,
                    AUTHOR.name AS author_name
                FROM BOOK
                INNER JOIN AUTHOR
                    ON BOOK.author_id = AUTHOR.author_id
                ORDER BY BOOK.book_id DESC
            """)
            books = cursor.fetchall()

            # Get all authors
            cursor.execute("""
                SELECT *
                FROM AUTHOR
                ORDER BY author_id
            """)
            authors = cursor.fetchall()

            # Calculate book statistics
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_books,
                    COALESCE(AVG(price), 0) AS average_price
                FROM BOOK
            """)
            book_stats = cursor.fetchone()

            # Calculate author statistics
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_authors,
                    COUNT(DISTINCT country) AS total_countries
                FROM AUTHOR
            """)
            author_stats = cursor.fetchone()

        return render_template(
            "library.html",
            books=books,
            authors=authors,
            total_books=book_stats["total_books"],
            average_price=book_stats["average_price"],
            total_authors=author_stats["total_authors"],
            total_countries=author_stats["total_countries"],
        )
    finally:
        db.close()


@app.route("/authors/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        country = request.form.get("country", "").strip()

        if not name or not country or len(name) > 100 or len(country) > 50:
            flash("Name (up to 100 characters) and country (up to 50) are required.")
            return redirect(url_for("add_author"))

        try:
            image_url = save_uploaded_image("image")
        except ValueError as error:
            flash(str(error))
            return redirect(url_for("add_author"))

        db = get_db()
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO AUTHOR (name, country, image_url)
                       VALUES (%s, %s, %s)""",
                    (name, country, image_url),
                )
            db.commit()
        finally:
            db.close()

        flash("Author added successfully.")
        return redirect(url_for("library_index"))

    return render_template("author_form.html", author=None)


@app.route("/authors/edit/<int:author_id>", methods=["GET", "POST"])
def edit_author(author_id):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM AUTHOR WHERE author_id = %s",
                (author_id,),
            )
            author = cursor.fetchone()

            if author is None:
                abort(404)

            if request.method == "POST":
                name = request.form.get("name", "").strip()
                country = request.form.get("country", "").strip()

                if not name or not country or len(name) > 100 or len(country) > 50:
                    flash("Name (up to 100 characters) and country (up to 50) are required.")
                    return redirect(
                        url_for("edit_author", author_id=author_id)
                    )

                try:
                    new_image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(
                        url_for("edit_author", author_id=author_id)
                    )

                image_url = new_image_url or author.get("image_url")

                cursor.execute(
                    """UPDATE AUTHOR
                       SET name = %s, country = %s, image_url = %s
                       WHERE author_id = %s""",
                    (name, country, image_url, author_id),
                )
                db.commit()

                flash("Author updated successfully.")
                return redirect(url_for("library_index"))

            return render_template("author_form.html", author=author)
    finally:
        db.close()


@app.route("/authors/delete/<int:author_id>", methods=["POST"])
def delete_author(author_id):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM AUTHOR WHERE author_id = %s",
                (author_id,),
            )
        db.commit()
    finally:
        db.close()

    flash("Author and their books deleted.")
    return redirect(url_for("library_index"))


def book_price(price_text):
    price = Decimal(price_text)
    if not price.is_finite() or not 0 <= price <= Decimal("99999999.99"):
        raise InvalidOperation
    if price.as_tuple().exponent < -2:
        raise InvalidOperation
    return price.quantize(Decimal("0.01"))


def valid_book_fields(title, author_id):
    return (
        0 < len(title) <= 150
        and 0 < len(author_id) <= 10
        and author_id.isascii()
        and author_id.isdigit()
        and 0 < int(author_id) <= 2147483647
    )


@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR ORDER BY name")
            authors = cursor.fetchall()

            if request.method == "POST":
                title = request.form.get("title", "").strip()
                price_text = request.form.get("price", "")
                author_id = request.form.get("author_id", "")

                try:
                    price = book_price(price_text)
                except (InvalidOperation, ValueError):
                    flash("Enter a price from 0 to 99999999.99 with at most two decimal places.")
                    return redirect(url_for("add_book"))

                if not valid_book_fields(title, author_id):
                    flash("Title (up to 150 characters) and a valid author are required.")
                    return redirect(url_for("add_book"))

                cursor.execute(
                    "SELECT author_id FROM AUTHOR WHERE author_id = %s",
                    (author_id,),
                )
                if cursor.fetchone() is None:
                    flash("Please select an existing author.")
                    return redirect(url_for("add_book"))

                try:
                    image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(url_for("add_book"))

                cursor.execute(
                    """INSERT INTO BOOK
                       (title, price, author_id, image_url)
                       VALUES (%s, %s, %s, %s)""",
                    (title, price, author_id, image_url),
                )
                db.commit()
                flash("Book added successfully.")
                return redirect(url_for("library_index"))

            return render_template(
                "book_form.html", book=None, authors=authors
            )
    finally:
        db.close()


@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM BOOK WHERE book_id = %s",
                (book_id,),
            )
            book = cursor.fetchone()

            if book is None:
                abort(404)

            cursor.execute("SELECT * FROM AUTHOR ORDER BY name")
            authors = cursor.fetchall()

            if request.method == "POST":
                title = request.form.get("title", "").strip()
                price_text = request.form.get("price", "")
                author_id = request.form.get("author_id", "")

                try:
                    price = book_price(price_text)
                except (InvalidOperation, ValueError):
                    flash("Enter a price from 0 to 99999999.99 with at most two decimal places.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                if not valid_book_fields(title, author_id):
                    flash("Title (up to 150 characters) and a valid author are required.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                cursor.execute(
                    "SELECT author_id FROM AUTHOR WHERE author_id = %s",
                    (author_id,),
                )
                if cursor.fetchone() is None:
                    flash("Please select an existing author.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                try:
                    new_image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                image_url = new_image_url or book.get("image_url")

                cursor.execute(
                    """UPDATE BOOK
                       SET title = %s,
                           price = %s,
                           author_id = %s,
                           image_url = %s
                       WHERE book_id = %s""",
                    (title, price, author_id, image_url, book_id),
                )
                db.commit()
                flash("Book updated successfully.")
                return redirect(url_for("library_index"))

            return render_template(
                "book_form.html", book=book, authors=authors
            )
    finally:
        db.close()


@app.route("/books/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM BOOK WHERE book_id = %s",
                (book_id,),
            )
        db.commit()
    finally:
        db.close()

    flash("Book deleted.")
    return redirect(url_for("library_index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")
        if len(name) > 100:
            errors.append("Name is too long (100 characters at most)")
        if len(email) > 255:
            errors.append("Email is too long (255 characters at most)")
        if len(password.encode("utf-8")) > 72:
            errors.append("Password is too long (72 UTF-8 bytes at most)")

        if not errors:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            conn = get_db()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                        (email, name, hashed),
                    )
                    conn.commit()
                    session.clear()
                    session["user_id"] = cur.lastrowid
                    session["name"] = name
                return redirect(url_for("todos"))
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062:
                    errors.append("Email Already Exists")
                else:
                    raise
            finally:
                conn.close()

    return render_template("register.html", errors=errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")

        if not errors:
            conn = get_db()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                        (email,),
                    )
                    user = cur.fetchone()
            finally:
                conn.close()

            if user and len(password.encode("utf-8")) <= 72 and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
                session.clear()
                session["user_id"] = user["user_id"]
                session["name"] = user["name"]
                return redirect(url_for("todos"))
            errors.append("Invalid email or password")

    return render_template("login.html", errors=errors)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def fetch_todos(user_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT todo_id, title, is_done, created_at FROM todos "
                "WHERE user_id = %s ORDER BY todo_id DESC",
                (user_id,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def run_write(sql, params):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def title_error(title):
    if not title:
        return "Title is required"
    if len(title) > 200:
        return "Title is too long (200 characters at most)"
    return None


def show_todos(errors):
    items = fetch_todos(session["user_id"])
    done_count = sum(1 for t in items if t["is_done"])
    return render_template(
        "todos.html",
        todos=items,
        errors=errors,
        name=session["name"],
        open_count=len(items) - done_count,
        done_count=done_count,
    )


@app.route("/todos")
def todos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return show_todos([])


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    err = title_error(title)
    if err:
        return show_todos([err])
    run_write(
        "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
        (session["user_id"], title),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    err = title_error(title)
    if err:
        return show_todos([err])
    run_write(
        "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
        (title, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    is_done = 1 if request.form.get("is_done") == "1" else 0
    run_write(
        "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
        (is_done, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    run_write(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
        (todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Something went wrong. Please try again."), 500


@app.errorhandler(400)
def invalid_form(error):
    return render_template("error.html", message=error.description), 400


@app.errorhandler(413)
def oversized_upload(error):
    return render_template("error.html", message="Upload must be smaller than 8 MB."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("APP_PORT", "5001")))
