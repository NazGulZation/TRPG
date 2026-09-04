"""
Aggregator and backward-compatibility suite for TRPG tests.
The test suite has been modularized by scope and chapter:

Core / System Tests:
- tests/test_engine_core.py
- tests/test_save_load.py
- tests/test_api.py

Chapter: Prologue Tests:
- tests/prologue/test_quests.py
- tests/prologue/test_companions_and_intimacy.py
- tests/prologue/test_party_recruitment.py
- tests/prologue/test_data_integrity.py
"""

import unittest
import sys

# Legacy imports support
from tests.test_engine_core import TestEngineCore as TestTRPGEngine
from tests.prologue.test_data_integrity import TestDataIntegrity as TestPrologueDataConfiguration
from tests.prologue.test_party_recruitment import TestPartyRecruitment as TestPartyCapacityAndRecruitmentRestrictions
from tests.test_save_load import TestSaveLoad as TestSaveLoadContinueSystem

TEST_MODULES = [
    "tests.test_engine_core",
    "tests.test_save_load",
    "tests.test_api",
    "tests.prologue.test_quests",
    "tests.prologue.test_companions_and_intimacy",
    "tests.prologue.test_party_recruitment",
    "tests.prologue.test_data_integrity",
]


def load_tests(loader, standard_tests, pattern):
    """
    Prevent duplicate test execution when running 'unittest discover'.
    Only populate when test_trpg is explicitly targeted.
    """
    suite = unittest.TestSuite()
    is_targeted = any("test_trpg" in arg for arg in sys.argv) or (pattern and "test_trpg" in pattern)
    if is_targeted:
        for mod_name in TEST_MODULES:
            suite.addTests(loader.loadTestsFromName(mod_name))
        return suite
    return suite


if __name__ == "__main__":
    unittest.main()
