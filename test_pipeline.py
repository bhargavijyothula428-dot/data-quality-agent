import unittest
import pandas as pd
import yaml
import os
from validator import run_validation

class TestDataQualityPipeline(unittest.TestCase):

    def setUp(self):
        # Create a tiny mock dataset with errors to test the code
        self.test_df = pd.DataFrame({
            "user_id": ["USR101", None],  
            "age": [25, -5],              
            "email": ["alice@example.com", "bob_at_example.com"]
        })
        self.test_df.to_csv("mock_test_data.csv", index=False)

        # Create matching temporary validation rules configuration
        self.rules_content = {
            "validation_rules": [
                {"column": "user_id", "check": "not_null"},
                {"column": "age", "check": "min_max", "min": 0, "max": 120},
                {"column": "email", "check": "contains", "value": "@"}
            ]
        }
        with open("mock_test_rules.yaml", "w") as f:
            yaml.dump(self.rules_content, f)

    def tearDown(self):
        # Clean up files after testing completes
        if os.path.exists("mock_test_data.csv"): os.remove("mock_test_data.csv")
        if os.path.exists("mock_test_rules.yaml"): os.remove("mock_test_rules.yaml")

    def test_pipeline_catches_anomalies(self):
        """Verify that our backend engine identifies the structural errors successfully."""
        errors = run_validation("mock_test_data.csv", "mock_test_rules.yaml")
        self.assertGreater(len(errors), 0, "The validation engine failed to detect the bad rows!")

if __name__ == '__main__':
    unittest.main()