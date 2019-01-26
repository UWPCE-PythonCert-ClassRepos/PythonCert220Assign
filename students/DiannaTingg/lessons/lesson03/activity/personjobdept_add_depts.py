"""
Add details for job departments.
"""

import personjobdept_model as pjd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with the Department class.')

DEPT_NUM = 0
DEPT_NAME = 1
DEPT_MANAGER = 2
JOB_EMPLOYED = 3

depts = [
    ('H123', 'Human Resources', 'Susan Bell', 'Analyst'),
    ('F245', 'Finance', 'Wally Smith', 'Senior Analyst'),
    ('Q321', 'Quality', 'Chris Wood', 'Admin Supervisor'),
    ('A432', 'Administration', 'Florence Cook', 'Admin Manager'),
    ('S512', 'Safety', 'Tom Jones', 'Executive Assistant')
    ]

for dept in depts:
    try:
        with pjd.database.transaction():
            new_dept = pjd.Department.create(
                dept_num=dept[DEPT_NUM],
                dept_name=dept[DEPT_NAME],
                dept_manager=dept[DEPT_MANAGER],
                job_employed=dept[JOB_EMPLOYED]
            )

            new_dept.save()

    except Exception as e:
        logger.info(f'Error creating department {dept[DEPT_NUM]}: {dept[DEPT_NAME]}.')
        logger.info(e)

logger.info('Reading and printing all Department rows.')

for dept in pjd.Department:
    logger.info(f'Number: {dept.dept_num}, Name: {dept.dept_name}, Manager: {dept.dept_manager}, Job: {dept.job_employed}')

pjd.database.close()
