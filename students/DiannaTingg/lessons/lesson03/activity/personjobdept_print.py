"""
Print all of the departments a person worked in for every job they ever had.
"""

from personjobdept_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Selecting all people and jobs.')

query = (Person
         .select(Person, Job)
         .join(Job, JOIN.LEFT_OUTER)
         .order_by(Person.person_name)
        )

for person in query:
    try:
        print(f'Person {person.person_name} worked in {person.job.dept_name}.')
    except AttributeError:
        print(f'Person {person.person_name} didn\'t have a job.')