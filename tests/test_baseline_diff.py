from src.baseline import diff_results

old = {"DIR-001": "PASS", "DIR-003": "PASS", "DIR-005": "FAIL (vuln found)"}
new = {"DIR-001": "PASS", "DIR-003": "FAIL (vuln found)", "DIR-005": "FAIL (vuln found)"}

regressions = diff_results(old, new)
print("Regressions:", regressions)