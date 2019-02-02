"""
Print all of the departments a person worked in for every job they ever had.
"""

import personjobdept_model as pjd
from peewee import JOIN
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Selecting all people and jobs.')

query = (pjd.Person
         .select(pjd.Person, pjd.Job, pjd.Department)
         .join(pjd.Job, JOIN.LEFT_OUTER)
         .join(pjd.Department, JOIN.LEFT_OUTER)
         )

for person in query:
    try:
        logger.info(f"{person.person_name} worked as a {person.job.job_name} in department "
                    f"{person.job.department.dept_name}.")
    except AttributeError:
        logger.info(f"{person.person_name} didn\'t have a job.")
