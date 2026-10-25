CREATE DATABASE IF NOT EXISTS combined_labs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE combined_labs;

-- Table 1: Departments
CREATE TABLE IF NOT EXISTS DEPARTMENT (
    Dnumber INT PRIMARY KEY,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn CHAR(9),
    mgr_start_date DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 2: Employees
CREATE TABLE IF NOT EXISTS EMPLOYEE (
    ssn CHAR(9) PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT NOT NULL,
    CONSTRAINT fk_employee_department
        FOREIGN KEY (Dno)
        REFERENCES DEPARTMENT(Dnumber)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 3: Projects
CREATE TABLE IF NOT EXISTS PROJECT (
    Pnumber INT PRIMARY KEY,
    Pname VARCHAR(50) NOT NULL,
    Plocation VARCHAR(50),
    Dno INT NOT NULL,
    CONSTRAINT fk_project_department
        FOREIGN KEY (Dno)
        REFERENCES DEPARTMENT(Dnumber)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- The manager FK must be added after EMPLOYEE exists; the guard allows re-runs.
SET @manager_fk_sql = IF(
    EXISTS (
        SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
        WHERE CONSTRAINT_SCHEMA = DATABASE()
          AND TABLE_NAME = 'DEPARTMENT'
          AND CONSTRAINT_NAME = 'fk_department_manager'
    ),
    'SELECT 1',
    'ALTER TABLE DEPARTMENT ADD CONSTRAINT fk_department_manager FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn)'
);
PREPARE manager_fk_statement FROM @manager_fk_sql;
EXECUTE manager_fk_statement;
DEALLOCATE PREPARE manager_fk_statement;

