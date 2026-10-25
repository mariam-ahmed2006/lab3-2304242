-- Existing rows are kept when seed scripts are re-run.
USE combined_labs;

INSERT INTO AUTHOR (author_id, name, country, image_url)
VALUES
    (1, 'Naguib Mahfouz', 'Egypt', 'images/Naguib Mahfouz.jpg'),
    (2, 'J.K. Rowling', 'United Kingdom', 'images/J.K. Rowling.jpg'),
    (3, 'George Orwell', 'United Kingdom', 'images/George Orwell.jpg')
ON DUPLICATE KEY UPDATE author_id = VALUES(author_id);

INSERT INTO BOOK (book_id, title, price, author_id, image_url)
VALUES
    (1, 'Palace Walk', 250.00, 1, 'images/Palace Walk.jpg'),
    (2, 'The Thief and the Dogs', 180.00, 1, 'images/The Thief and the Dogs.jpg'),
    (3, 'Harry Potter and the Philosophers Stone', 350.00, 2, 'images/Harry Potter and the Philosopher Stone.jpg'),
    (4, 'Harry Potter and the Chamber of Secrets', 320.00, 2, 'images/Harry Potter and the Chamber of Secrets.jpg'),
    (5, 'Animal Farm', 150.00, 3, 'images/Animal Farm.jpg'),
    (6, 'Nineteen Eighty-Four', 200.00, 3, 'images/Nineteen Eighty-Four.jpg')
ON DUPLICATE KEY UPDATE book_id = VALUES(book_id);
