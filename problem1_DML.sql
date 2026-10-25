-- Fixed sample IDs make re-running the seeds safe without replacing edited rows.

USE combined_labs;

-- 1. Insert departments without managers initially
INSERT INTO DEPARTMENT
    (Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES
    (1, 'Engineering', NULL, NULL),
    (2, 'Human Resources', NULL, NULL),
    (3, 'Finance', NULL, NULL)
ON DUPLICATE KEY UPDATE Dnumber = VALUES(Dnumber);

-- 2. Insert employees
INSERT INTO EMPLOYEE
    (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES
    ('100000001', 'Ahmed', 'Ali', '2002-05-12',
     'Alexandria', 'M', 15000.00, 1),
    ('100000002', 'Mariam', 'Hassan', '2001-09-20',
     'Cairo', 'F', 18000.00, 2),
    ('100000003', 'Omar', 'Khaled', '2000-03-15',
     'Giza', 'M', 20000.00, 3)
ON DUPLICATE KEY UPDATE ssn = VALUES(ssn);

-- 3. Assign managers now that employees exist
UPDATE DEPARTMENT
SET mgr_ssn = '100000001',
    mgr_start_date = '2025-01-01'
WHERE Dnumber = 1 AND mgr_ssn IS NULL;

UPDATE DEPARTMENT
SET mgr_ssn = '100000002',
    mgr_start_date = '2025-02-01'
WHERE Dnumber = 2 AND mgr_ssn IS NULL;

UPDATE DEPARTMENT
SET mgr_ssn = '100000003',
    mgr_start_date = '2025-03-01'
WHERE Dnumber = 3 AND mgr_ssn IS NULL;

-- 4. Insert projects
INSERT INTO PROJECT
    (Pnumber, Pname, Plocation, Dno)
VALUES
    (101, 'Website Development', 'Alexandria', 1),
    (102, 'Recruitment System', 'Cairo', 2),
    (103, 'Budget Analysis', 'Giza', 3)
ON DUPLICATE KEY UPDATE Pnumber = VALUES(Pnumber);
