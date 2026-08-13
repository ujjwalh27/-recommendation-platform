import sys
sys.path.insert(0, ".")
from tests.test_profile_stability import TestProfileStability
from tests.test_live_profile_flow import TestLiveProfileFlow
import unittest

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestProfileStability)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestLiveProfileFlow)
    full_suite = unittest.TestSuite([suite1, suite2])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(full_suite)
    if not result.wasSuccessful():
        sys.exit(1)
