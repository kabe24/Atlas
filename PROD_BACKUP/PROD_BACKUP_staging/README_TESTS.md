# Atlas API Test Suite Documentation

## Quick Start

Run the complete test suite with:

```bash
python3 test_suite.py
```

## Test Scripts

### 1. test_suite.py (Recommended for CI/CD)

Compact, production-ready test runner.

**Features**:
- 39 comprehensive API tests (Features 1-10, 34, 57-59)
- Color-coded PASS/FAIL output
- Summary statistics
- Quick failure identification
- ~2-3 second execution time

**Output**:
```
ATLAS API TEST SUITE
════════════════════════════════════════════════════════════════════════════════

SANITY CHECKS (Original Endpoints)
────────────────────────────────────────────────────────────────────────────────
  [ 1] GET /api/students                                            ✓ PASS
  [ 2] GET /api/subjects                                            ✓ PASS

FEATURE 7: MULTI-TENANCY
────────────────────────────────────────────────────────────────────────────────
  [ 3] POST /api/admin/instance/create                              ✓ PASS
       -> instance_id: 8ab50e9aed36
  ...

════════════════════════════════════════════════════════════════════════════════
TEST SUMMARY
════════════════════════════════════════════════════════════════════════════════
Total Tests: 39
Passed:      39
Failed:      0
Pass Rate:   100.0%
════════════════════════════════════════════════════════════════════════════════
```

**Run**:
```bash
python3 test_suite.py
```

### 2. test_suite_verbose.py (For Development & Debugging)

Detailed test runner with full response inspection.

**Features**:
- Same 39 tests as compact version
- Full JSON response output
- Data validation comments
- Organized by feature section
- Better for understanding test flow
- ~3-4 second execution time

**Output**:
```
══════════════════════════════════════════════════════════════════════════════════
ATLAS API TEST SUITE - DETAILED MODE
══════════════════════════════════════════════════════════════════════════════════

SECTION: SANITY CHECKS (Original Endpoints)
──────────────────────────────────────────────────────────────────────────────────

  Test  1: ✓ PASS
  Endpoint: GET /api/students
  Status:   200 (expected 200)
  Response: {
  "students": [
    {
      "student_id": "40f98e4e",
      "name": "Test Student",
      ...
    }
  ]
}
  ✓ Contains subjects: ['math', 'science', 'ela']...
```

**Run**:
```bash
python3 test_suite_verbose.py
```

## Test Coverage

### Sanity Checks (2 tests)
- Verify existing endpoints still work
- Check core student and subject data

### Feature 7: Multi-Tenancy (6 tests)
- Instance creation with unique ID
- Instance listing and retrieval
- Parent PIN authentication
- Invalid PIN rejection (401)
- Instance-scoped student listing

### Feature 8: Platform Customization (5 tests)
- Subject catalog retrieval
- Instance configuration updates
- Custom subject creation
- Custom subject verification
- Custom subject deletion

### Feature 9: Ad Hoc Diagnostics (5 tests)
- Student creation
- Diagnostic scheduling
- Diagnostic status tracking
- Student pending diagnostics view
- Diagnostic cancellation

### Feature 10: Feedback Mechanism (7 tests)
- Student feedback submission
- Student feedback retrieval
- Parent feedback submission
- Parent feedback listing
- Feedback approval action
- Admin feedback aggregation
- Feedback statistics

### Default Instance Check (1 test)
- Verify default instance accessibility
- Check data migration

## Testing Methodology

**Transport Method**: ASGI (Application Server Gateway Interface)
- No HTTP server required
- Direct app testing via httpx.ASGITransport
- Eliminates network overhead
- Fastest test execution

**Framework**: FastAPI + httpx
- Async/await support
- JSON request/response handling
- Status code validation
- Complete endpoint coverage

**Base URL**: http://test (virtual, for ASGI testing)

## Authentication

**PIN-Based Access**:
- All instance operations require parent PIN
- Default PIN for test instances: "0000"
- Invalid PINs return 401 Unauthorized
- PIN validation enforced on sensitive operations

## Test Data

**Created During Tests**:
- Instance: Test Family (ID: 8ab50e9aed36)
- Student: Test Student (ID: 67887b5d)
- Feedback: Bug report + Feature request
- Custom Subject: Test Subject (deleted after test)

All test data is isolated to created instance.

## Expected Behavior

### All 39 Tests Should Pass ✓

If you see failures:

1. **Check API modifications**
   - Review recent code changes in app.py
   - Verify endpoint signatures haven't changed
   - Check request/response models

2. **Check file permissions**
   - Ensure write access to the data/ directory
   - Check STUDENTS_DIR and INSTANCES_DIR exist

3. **Check dependencies**
   ```bash
   pip list | grep -E "fastapi|httpx|anthropic"
   ```

4. **Run verbose test for details**
   ```bash
   python3 test_suite_verbose.py
   ```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: cd /path/to/ai-tutor && python3 test_suite.py
```

### Local Pre-commit

```bash
#!/bin/bash
python3 test_suite.py || exit 1
```

## Performance Baseline

**Typical Execution Time**: 2-3 seconds

**Bottlenecks** (if slower):
- File I/O on instance creation
- JSON serialization/deserialization
- Anthropic API calls (not used in test suite)

## Extending Tests

### Add New Feature Test

1. Create new test function in test_suite.py:
```python
# Test N: New Feature
if runner.instance_id:
    response = await client.post(
        f"/api/instance/{runner.instance_id}/new/endpoint",
        json={"pin": "0000", "data": "value"}
    )
    runner.add_result(test_num, "POST /api/instance/{id}/new/endpoint",
                     response.status_code, 200, response.json())
test_num += 1
```

2. Update TEST_RESULTS.md with new test details

3. Run verbose test to debug:
```bash
python3 test_suite_verbose.py
```

## Troubleshooting

### Issue: Tests hang or timeout

**Solution**:
```bash
# Kill process if it hangs
Ctrl+C

# Run with explicit timeout
timeout 30 python3 test_suite.py
```

### Issue: "Cannot create instance" errors

**Solution**:
```bash
# Check data directory
ls -la data/instances/

# Verify directory is writable
touch data/test_write.txt && rm data/test_write.txt

# Check instance registry
cat data/instances/instances.json
```

### Issue: PIN validation failures

**Solution**:
- Default PIN should be "0000"
- Check instance parent config file:
  ```bash
  cat data/instances/[instance_id]/parent.json
  ```

### Issue: "Student not found" errors

**Solution**:
- Verify student was created successfully in previous test
- Check students directory:
  ```bash
  ls -la data/students/
  cat data/students/[student_id].json
  ```

## Files Generated During Testing

```
data/
  instances/
    instances.json          # Instance registry
    8ab50e9aed36/          # Test instance directory
      config.json          # Instance configuration
      parent.json          # Parent PIN config
      feedback/            # Instance feedback
  students/
    67887b5d.json         # Test student profile
    67887b5d/
      profiles/           # Diagnostic results
      feedback/           # Student feedback
```

## Cleanup

Remove test data:

```bash
# Remove test instance
rm -rf data/instances/8ab50e9aed36

# Remove test student
rm -rf data/students/67887b5d
rm data/students/67887b5d.json

# Update registry
# (Script would need to regenerate)
```

## Additional Resources

- **API Documentation**: See endpoint comments in app.py
- **Feature 7 docs**: Multi-tenancy system design
- **Feature 8 docs**: Customization architecture
- **Feature 9 docs**: Diagnostic scheduling
- **Feature 10 docs**: Feedback workflow

## Contact

For test issues or improvements:
1. Check TEST_RESULTS.md for detailed results
2. Review test_suite_verbose.py output
3. Examine failing endpoint in app.py
4. Check data directory permissions and structure

## License

Test suite is part of Atlas project.
