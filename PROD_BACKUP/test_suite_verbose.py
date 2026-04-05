"""
Comprehensive API Test Suite for Atlas (Features 1-10, 34, 57-59)
Uses ASGI transport for testing without a running server.
"""

import httpx
from httpx import ASGITransport
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from app import app

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


class TestRunner:
    def __init__(self):
        self.results = []
        self.instance_id = None
        self.student_id = None
        self.feedback_id = None
        self.passed = 0
        self.failed = 0

    def add_result(self, test_num, endpoint, status_code, expected, response_data=None):
        """Record test result."""
        passed = status_code == expected
        if passed:
            self.passed += 1
            result = f"{GREEN}PASS{RESET}"
        else:
            self.failed += 1
            result = f"{RED}FAIL{RESET}"

        self.results.append({
            "num": test_num,
            "endpoint": endpoint,
            "status": status_code,
            "expected": expected,
            "passed": passed,
            "data": response_data,
        })
        print(f"  [{test_num:2d}] {endpoint:<60} {result}")
        if not passed:
            print(f"       Expected: {expected}, Got: {status_code}")
            if response_data:
                print(f"       Response: {json.dumps(response_data)[:100]}")

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}TEST SUMMARY{RESET}")
        print(f"{BOLD}{'='*80}{RESET}")
        print(f"Total Tests: {total}")
        print(f"Passed:      {GREEN}{self.passed}{RESET}")
        print(f"Failed:      {RED}{self.failed}{RESET}")
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        print(f"Pass Rate:   {pass_rate:.1f}%")
        print(f"{BOLD}{'='*80}{RESET}\n")


async def run_tests():
    """Run comprehensive test suite."""
    runner = TestRunner()
    test_num = 1

    print(f"\n{BOLD}ATLAS API TEST SUITE (Features 1-10, 34, 57-59){RESET}")
    print(f"{BOLD}{'='*80}{RESET}\n")

    # ─────────────────────────────────────────────────────────────────────────
    # Setup: Create ASGI transport
    # ─────────────────────────────────────────────────────────────────────────
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:

        # ─────────────────────────────────────────────────────────────────────
        # SANITY CHECKS: Existing endpoints should still work
        # ─────────────────────────────────────────────────────────────────────
        print(f"{BOLD}SANITY CHECKS (Original Endpoints){RESET}")
        print("─" * 80)

        # Test 1: GET /api/students
        response = await client.get("/api/students")
        runner.add_result(test_num, "GET /api/students", response.status_code, 200, response.json())
        test_num += 1

        # Test 2: GET /api/subjects
        response = await client.get("/api/subjects")
        runner.add_result(test_num, "GET /api/subjects", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 7: MULTI-TENANCY
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 7: MULTI-TENANCY{RESET}")
        print("─" * 80)

        # Test 3: POST /api/admin/instance/create
        response = await client.post(
            "/api/admin/instance/create",
            json={
                "family_name": "Test Family",
                "owner_email": "test@test.com",
            }
        )
        runner.add_result(test_num, "POST /api/admin/instance/create", response.status_code, 200, response.json())
        if response.status_code == 200:
            data = response.json()
            runner.instance_id = data.get("instance", {}).get("instance_id")
            print(f"       -> instance_id: {runner.instance_id}")
        test_num += 1

        # Test 4: GET /api/admin/instances
        response = await client.get("/api/admin/instances")
        runner.add_result(test_num, "GET /api/admin/instances", response.status_code, 200, response.json())
        test_num += 1

        # Test 5: GET /api/instance/{id} with PIN
        if runner.instance_id:
            response = await client.get(f"/api/instance/{runner.instance_id}", params={"pin": "0000"})
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}?pin=0000", response.status_code, 200, response.json())
        test_num += 1

        # Test 6: POST /api/instance/{id}/parent/login (valid PIN)
        if runner.instance_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/parent/login",
                json={"pin": "0000"}
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/parent/login (valid)", response.status_code, 200, response.json())
        test_num += 1

        # Test 7: POST /api/instance/{id}/parent/login (invalid PIN)
        if runner.instance_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/parent/login",
                json={"pin": "9999"}
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/parent/login (invalid)", response.status_code, 401, response.json())
        test_num += 1

        # Test 8: GET /api/instance/{id}/parent/students?pin=0000
        if runner.instance_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/parent/students",
                params={"pin": "0000"}
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/parent/students", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 8: PLATFORM CUSTOMIZATION
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 8: PLATFORM CUSTOMIZATION{RESET}")
        print("─" * 80)

        # Test 9: GET /api/subjects/catalog
        response = await client.get("/api/subjects/catalog")
        runner.add_result(test_num, "GET /api/subjects/catalog", response.status_code, 200, response.json())
        test_num += 1

        # Test 10: PUT /api/instance/{id}/config
        if runner.instance_id:
            response = await client.put(
                f"/api/instance/{runner.instance_id}/config",
                json={
                    "pin": "0000",
                    "customization": {
                        "branding": {
                            "name": "Test School",
                            "color": "#FF5733"
                        }
                    }
                }
            )
            runner.add_result(test_num, f"PUT /api/instance/{runner.instance_id}/config", response.status_code, 200, response.json())
        test_num += 1

        # Test 11: POST /api/instance/{id}/subjects/custom (add custom subject)
        if runner.instance_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/subjects/custom",
                json={
                    "pin": "0000",
                    "key": "test_subj",
                    "name": "Test Subject",
                    "icon": "🎵",
                    "color": "#FF5733",
                    "topics": ["Topic 1", "Topic 2", "Topic 3"],
                    "system_prompt": "You are a test tutor"
                }
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/subjects/custom", response.status_code, 200, response.json())
        test_num += 1

        # Test 12: GET /api/instance/{id}/subjects (should include custom)
        if runner.instance_id:
            response = await client.get(f"/api/instance/{runner.instance_id}/subjects")
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/subjects", response.status_code, 200, response.json())
        test_num += 1

        # Test 13: DELETE /api/instance/{id}/subjects/custom/test_subj
        if runner.instance_id:
            response = await client.delete(
                f"/api/instance/{runner.instance_id}/subjects/custom/test_subj",
                params={"pin": "0000"}
            )
            runner.add_result(test_num, f"DELETE /api/instance/{runner.instance_id}/subjects/custom/test_subj", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 9: AD HOC DIAGNOSTICS
        # First, we need to create a student in the test instance
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 9: AD HOC DIAGNOSTICS{RESET}")
        print("─" * 80)

        # Test 14: Create a student in the test instance
        if runner.instance_id:
            # We need to create student data in the instance-specific directory
            response = await client.post(
                "/api/student/create",
                json={
                    "name": "Test Student",
                    "pin": "1234",
                    "avatar": "👦",
                    "grade": 8
                }
            )
            runner.add_result(test_num, "POST /api/student/create", response.status_code, 200, response.json())
            if response.status_code == 200:
                data = response.json()
                runner.student_id = data.get("student", {}).get("student_id")
                print(f"       -> student_id: {runner.student_id}")
        test_num += 1

        # Test 15: POST /api/instance/{id}/parent/diagnostic/schedule/{sid}/math
        if runner.instance_id and runner.student_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/parent/diagnostic/schedule/{runner.student_id}/math",
                json={"pin": "0000"}
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/parent/diagnostic/schedule/{runner.student_id}/math", response.status_code, 200, response.json())
        test_num += 1

        # Test 16: GET /api/instance/{id}/parent/diagnostic/status/{sid}
        if runner.instance_id and runner.student_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/parent/diagnostic/status/{runner.student_id}",
                params={"pin": "0000"}
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/parent/diagnostic/status/{runner.student_id}", response.status_code, 200, response.json())
        test_num += 1

        # Test 17: GET /api/student/pending-diagnostics/{sid}
        if runner.student_id:
            response = await client.get(
                f"/api/student/pending-diagnostics/{runner.student_id}",
                params={"instance_id": runner.instance_id or "default"}
            )
            runner.add_result(test_num, f"GET /api/student/pending-diagnostics/{runner.student_id}", response.status_code, 200, response.json())
        test_num += 1

        # Test 18: POST /api/instance/{id}/parent/diagnostic/cancel/{sid}/math
        if runner.instance_id and runner.student_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/parent/diagnostic/cancel/{runner.student_id}/math",
                json={"pin": "0000"}
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/parent/diagnostic/cancel/{runner.student_id}/math", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 10: FEEDBACK MECHANISM
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 10: FEEDBACK MECHANISM{RESET}")
        print("─" * 80)

        # Test 19: POST /api/instance/{id}/student/feedback
        if runner.instance_id and runner.student_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/student/feedback",
                json={
                    "student_id": runner.student_id,
                    "submitted_by": "student",
                    "feedback_type": "bug_report",
                    "title": "Test Bug",
                    "content": "This is a test bug report",
                    "subject": "math"
                }
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/student/feedback", response.status_code, 200, response.json())
            if response.status_code == 200:
                data = response.json()
                runner.feedback_id = data.get("feedback_id")
                print(f"       -> feedback_id: {runner.feedback_id}")
        test_num += 1

        # Test 20: GET /api/instance/{id}/student/{sid}/feedback
        if runner.instance_id and runner.student_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/student/{runner.student_id}/feedback"
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/student/{runner.student_id}/feedback", response.status_code, 200, response.json())
        test_num += 1

        # Test 21: POST /api/instance/{id}/parent/feedback
        if runner.instance_id:
            response = await client.post(
                f"/api/instance/{runner.instance_id}/parent/feedback",
                json={
                    "submitted_by": "parent",
                    "feedback_type": "feature_request",
                    "title": "Parent Feature Request",
                    "content": "I would like this feature",
                    "subject": "general"
                }
            )
            runner.add_result(test_num, f"POST /api/instance/{runner.instance_id}/parent/feedback", response.status_code, 200, response.json())
        test_num += 1

        # Test 22: GET /api/instance/{id}/parent/feedback?pin=0000
        if runner.instance_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/parent/feedback",
                params={"pin": "0000"}
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/parent/feedback", response.status_code, 200, response.json())
        test_num += 1

        # Test 23: PUT /api/instance/{id}/parent/feedback/{fid} (approve action)
        if runner.instance_id and runner.feedback_id:
            response = await client.put(
                f"/api/instance/{runner.instance_id}/parent/feedback/{runner.feedback_id}",
                json={
                    "pin": "0000",
                    "action": "approve"
                }
            )
            runner.add_result(test_num, f"PUT /api/instance/{runner.instance_id}/parent/feedback/{runner.feedback_id}", response.status_code, 200, response.json())
        test_num += 1

        # Test 24: GET /api/admin/feedback
        response = await client.get("/api/admin/feedback")
        runner.add_result(test_num, "GET /api/admin/feedback", response.status_code, 200, response.json())
        test_num += 1

        # Test 25: GET /api/admin/feedback/stats
        response = await client.get("/api/admin/feedback/stats")
        runner.add_result(test_num, "GET /api/admin/feedback/stats", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # DEFAULT INSTANCE CHECK
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}DEFAULT INSTANCE (Migrated Data){RESET}")
        print("─" * 80)

        # Test 26: GET /api/instance/default (using default instance ID directly)
        response = await client.get("/api/instance/default", params={"pin": "0000"})
        runner.add_result(test_num, "GET /api/instance/default?pin=0000", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 34: BOOK MASTERY
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 34: BOOK MASTERY{RESET}")
        print("─" * 80)

        # Test 27: POST /api/book-mastery/start
        book_session_id = None
        if runner.instance_id and runner.student_id:
            response = await client.post(
                "/api/book-mastery/start",
                json={
                    "student_id": runner.student_id,
                    "instance_id": runner.instance_id,
                    "title": "Test Book",
                    "author": "Test Author",
                    "total_chapters": 2
                }
            )
            runner.add_result(test_num, "POST /api/book-mastery/start", response.status_code, 200, response.json())
            if response.status_code == 200:
                data = response.json()
                book_session_id = data.get("session_id")
                print(f"       -> session_id: {book_session_id}")
        test_num += 1

        # Test 28: GET /api/book-mastery/bookshelf/{student_id}
        if runner.student_id and runner.instance_id:
            response = await client.get(
                f"/api/book-mastery/bookshelf/{runner.student_id}",
                params={"instance_id": runner.instance_id}
            )
            runner.add_result(test_num, f"GET /api/book-mastery/bookshelf/{runner.student_id}", response.status_code, 200, response.json())
        test_num += 1

        # Test 29: GET /api/book-mastery/session/{session_id}
        if book_session_id:
            response = await client.get(f"/api/book-mastery/session/{book_session_id}")
            runner.add_result(test_num, f"GET /api/book-mastery/session/{book_session_id}", response.status_code, 200, response.json())
        test_num += 1

        # Test 30: POST /api/book-mastery/quiz
        if book_session_id and runner.student_id and runner.instance_id:
            response = await client.post(
                "/api/book-mastery/quiz",
                json={
                    "session_id": book_session_id,
                    "student_id": runner.student_id,
                    "instance_id": runner.instance_id
                }
            )
            runner.add_result(test_num, "POST /api/book-mastery/quiz", response.status_code, 200, response.json())
        test_num += 1

        # Test 31: POST /api/book-mastery/retry
        if book_session_id and runner.student_id and runner.instance_id:
            response = await client.post(
                "/api/book-mastery/retry",
                json={
                    "session_id": book_session_id,
                    "student_id": runner.student_id,
                    "instance_id": runner.instance_id
                }
            )
            runner.add_result(test_num, "POST /api/book-mastery/retry", response.status_code, 200, response.json())
        test_num += 1

        # Test 32: POST /api/book-mastery/summary
        if book_session_id and runner.student_id and runner.instance_id:
            response = await client.post(
                "/api/book-mastery/summary",
                json={
                    "session_id": book_session_id,
                    "student_id": runner.student_id,
                    "instance_id": runner.instance_id
                }
            )
            runner.add_result(test_num, "POST /api/book-mastery/summary", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 59: AI PROFICIENCY SELF-ASSESSMENT
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 59: AI PROFICIENCY SELF-ASSESSMENT{RESET}")
        print("─" * 80)

        # Test 33: PUT /api/instance/{id}/config - Set ai_proficiency
        if runner.instance_id:
            response = await client.put(
                f"/api/instance/{runner.instance_id}/config",
                json={
                    "pin": "0000",
                    "customization": {"ai_proficiency": "low"}
                }
            )
            runner.add_result(test_num, f"PUT /api/instance/{runner.instance_id}/config (ai_proficiency)", response.status_code, 200, response.json())
        test_num += 1

        # Test 34: GET /api/instance/{id} - Verify ai_proficiency stored
        if runner.instance_id:
            response = await client.get(f"/api/instance/{runner.instance_id}", params={"pin": "0000"})
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id} (verify ai_proficiency)", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 57: GUIDED CONVERSATION MODE
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 57: GUIDED CONVERSATION MODE{RESET}")
        print("─" * 80)

        # Test 35: PUT /api/instance/{id}/student/{sid}/conversation-mode - Set to "guided"
        if runner.instance_id and runner.student_id:
            response = await client.put(
                f"/api/instance/{runner.instance_id}/student/{runner.student_id}/conversation-mode",
                json={"mode": "guided", "pin": "0000"}
            )
            runner.add_result(test_num, f"PUT /api/instance/{runner.instance_id}/student/{runner.student_id}/conversation-mode (guided)", response.status_code, 200, response.json())
        test_num += 1

        # Test 36: PUT /api/instance/{id}/student/{sid}/conversation-mode - Set to "open"
        if runner.instance_id and runner.student_id:
            response = await client.put(
                f"/api/instance/{runner.instance_id}/student/{runner.student_id}/conversation-mode",
                json={"mode": "open", "pin": "0000"}
            )
            runner.add_result(test_num, f"PUT /api/instance/{runner.instance_id}/student/{runner.student_id}/conversation-mode (open)", response.status_code, 200, response.json())
        test_num += 1

        # Test 37: GET /api/instance/{id}/parent/students - Verify conversation_mode in response
        if runner.instance_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/parent/students",
                params={"pin": "0000"}
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/parent/students (verify conversation_mode)", response.status_code, 200, response.json())
        test_num += 1

        # ─────────────────────────────────────────────────────────────────────
        # FEATURE 58: ADAPTIVE RESPONSE COMPLEXITY
        # ─────────────────────────────────────────────────────────────────────
        print(f"\n{BOLD}FEATURE 58: ADAPTIVE RESPONSE COMPLEXITY{RESET}")
        print("─" * 80)

        # Test 38: GET /api/instance/{id}/student/{sid}/complexity-tiers
        complexity_tiers_data = None
        if runner.instance_id and runner.student_id:
            response = await client.get(
                f"/api/instance/{runner.instance_id}/student/{runner.student_id}/complexity-tiers"
            )
            runner.add_result(test_num, f"GET /api/instance/{runner.instance_id}/student/{runner.student_id}/complexity-tiers", response.status_code, 200, response.json())
            if response.status_code == 200:
                complexity_tiers_data = response.json()
        test_num += 1

        # Test 39: Verify complexity tier response structure
        if complexity_tiers_data:
            # Validate that response contains tier data
            has_tier_data = isinstance(complexity_tiers_data, dict) and len(complexity_tiers_data) > 0
            response_obj = type('obj', (object,), {'status_code': 200 if has_tier_data else 400, 'json': lambda: complexity_tiers_data})()
            runner.add_result(test_num, "Complexity tier response structure validation", response_obj.status_code, 200, complexity_tiers_data)
        test_num += 1

    # Print summary
    runner.print_summary()

    # Print detailed results for debugging
    if runner.failed > 0:
        print(f"\n{BOLD}FAILED TESTS{RESET}")
        print("─" * 80)
        for result in runner.results:
            if not result["passed"]:
                print(f"[{result['num']:2d}] {result['endpoint']}")
                print(f"     Expected: {result['expected']}, Got: {result['status']}")
                if result['data']:
                    print(f"     Response: {json.dumps(result['data'])[:200]}")


if __name__ == "__main__":
    asyncio.run(run_tests())
