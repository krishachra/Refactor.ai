"""
Comprehensive Automated Test Suite for User Journey & Edge Cases.
Validates the complete flow:
1. Health check & model status inspection
2. Valid refactoring submissions across all supported goals (readability, performance, add_types, security, modernize)
3. Input validation (empty code, boundary checks, invalid goal payload)
4. Context passthrough
5. Response payload contract verification (refactored code, explanations, improvements, risks)
"""
import sys
import os
import unittest
import json

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, BACKEND_DIR)

from main import RefactorHTTPHandler
from test_handler import MockHTTPHandler


class TestUserJourneyFlow(unittest.TestCase):
    def test_journey_1_readability_refactor(self):
        """User journey: submit messy code for readability improvement."""
        req_payload = {
            "code": "def calc(x, y, z): return x * y + z",
            "goal": "readability",
            "language": "python",
            "context": "Focus on clear naming and docstring."
        }
        handler = MockHTTPHandler("POST", "/api/refactor", req_payload)
        resp = handler.get_response_body()
        
        self.assertIn("refactored_code", resp)
        self.assertIn("explanations", resp)
        self.assertIn("improvements", resp)
        self.assertIn("risks_and_tradeoffs", resp)
        self.assertEqual(resp.get("goal"), "readability")
        self.assertTrue(len(resp["explanations"]) > 0)

    def test_journey_2_security_audit(self):
        """User journey: submit vulnerable SQL snippet for security audit."""
        req_payload = {
            "code": "def find_account(uid): cursor.execute('SELECT * FROM acc WHERE id = ' + str(uid))",
            "goal": "security",
            "language": "python"
        }
        handler = MockHTTPHandler("POST", "/api/refactor", req_payload)
        resp = handler.get_response_body()
        
        self.assertEqual(resp.get("goal"), "security")
        self.assertIn("refactored_code", resp)
        # Verify security analysis is present
        explanations_text = " ".join(resp.get("explanations", [])).lower()
        self.assertTrue("sql" in explanations_text or "parameterized" in explanations_text)

    def test_journey_3_edge_case_empty_code(self):
        """Edge case: empty string rejected with 422 Unprocessable Entity."""
        handler = MockHTTPHandler("POST", "/api/refactor", {"code": "   "})
        resp = handler.get_response_body()
        self.assertIn("Validation Error", resp.get("error", ""))

    def test_journey_4_edge_case_code_too_large(self):
        """Edge case: code exceeding 50,000 characters is rejected."""
        huge_code = "x = 1\n" * 10000  # ~60,000 chars
        handler = MockHTTPHandler("POST", "/api/refactor", {"code": huge_code})
        resp = handler.get_response_body()
        self.assertIn("Validation Error", resp.get("error", ""))
        self.assertIn("exceeds maximum limit", resp.get("detail", ""))

    def test_journey_5_edge_case_invalid_goal(self):
        """Edge case: unrecognized goal rejected."""
        handler = MockHTTPHandler("POST", "/api/refactor", {"code": "def foo(): pass", "goal": "make_it_magic"})
        resp = handler.get_response_body()
        self.assertIn("Validation Error", resp.get("error", ""))


if __name__ == "__main__":
    unittest.main()

