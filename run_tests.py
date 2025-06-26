import unittest
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the test modules
from tests.test_api import TestCastingAPI
from tests.test_database import TestDatabase
from tests.test_import_data import TestImportData
from tests.test_main import TestMain
from tests.test_models import TestModels
from tests.test_schemas import TestSchemas

if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestSuite()
    
# Add test cases
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMain))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDatabase))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestModels))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSchemas))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCastingAPI))
test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImportData))
    
# Run the tests
test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
# Exit with appropriate status code
sys.exit(not test_result.wasSuccessful())
