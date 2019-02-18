"""This is the test script for basic operations"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from database import main, import_data, add_collection_csv, show_rentals, \
    show_available_products, MongoDBConnection


# Need to set up fixtures
