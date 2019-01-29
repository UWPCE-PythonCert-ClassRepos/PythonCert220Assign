"""
this module is called to setup and
teardown files in a student directory 
prior to autograding
"""

import pytest
import shutil
import os
import csv

@pytest.fixture
def _student():
    with open('students/student.csv') as f:
    student = [tuple(line) for line in csv.reader(f)]
    if len(student) != 1:
        raise ValueError(f"Error in student file: {student}")        
    return student

@pytest.fixture
def _course():
    return (
        ("inventory_management/integration_test.py", "tests/unit_tests.py", "tests/integration_test.py"),
        ("charges_calc.py", "charges_calc.log", "debugger_log.txt", "output.json"),
        ("basic_operations.py", "tests/", "data/customers.db", "data/customers.csv"),
        ("basic_operations.py", "tests/", "data/customers.db", "data/customers.csv", "db.log"),
        ("database.py"),
        ("good_pref.py"),
        ("linear.py", "parallel.py", "tests/", "findings.txt"),
        ("inventory.py"),
        ("charges_calc.py", "charges_calc.log", "debugger_log.txt", "output.json", "database.py", "images/"),
        ("database.py", "timings.txt")
    )

def setup_data(_student, _course):

    now_grading = student[3]
    if now_grading < 1 or now_grading > 10:
        raise ValueError(f"Week number error in student file: {submission[3]} for {submission[0]}")

    student_dir = f"lesson{100 + now_grading[1:]}"
    student_backup_dir = student_dir + "_bu"

    os.mkdir(student_backup_dir)
    for file in _course[now_grading]:
        shutil.copy(file, student_backup_dir)
        shutil.delete(file)

    shutil.copy("tests/", f"{student_dir}/")

    yield

    for file in _course[now_grading]:
        shutil.delete(file)

    shutil.copy(f"{student_backup_dir}/, {student_dir}/")
