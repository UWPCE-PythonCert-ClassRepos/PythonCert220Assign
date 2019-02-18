"""
Configuration settings for sqlite database.
"""

# Two databases: one for test and one for production
TEST_DATABASE = "test.db"
PROD_DATABASE = "customers.db"

# Switch between the databases by commenting out the other line.
DATABASE = TEST_DATABASE  # Use this one for test.
# DATABASE = PROD_DATABASE  # Use this one for production.