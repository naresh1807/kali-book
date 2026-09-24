# Worked synthetic finding: cross-user invoice read

This is an expected training finding, not a report about a real application.

**Rule:** Alice may read invoice 1 in tenant A, but not Bob invoice 2 in tenant B.

**Vulnerable behavior:** After completing the synthetic login, Alice requests GET /api/invoices/2. Vulnerable mode returns 200 with Bob synthetic invoice. Alice own invoice remains accessible.

**Cause:** The vulnerable branch permits a request without enforcing the object owner and tenant condition.

**Impact:** Cross-user confidentiality failure for the fictional invoice. Actual severity in a real system would depend on data sensitivity and reachable scope.

**Fix:** Apply the server-side owner and tenant condition to each object read using validated identity. Audit denied requests without recording tokens.

**Retest:** Fixed mode returns 403 for Alice requesting invoice 2 and 200 for Alice requesting invoice 1. Bob still reads invoice 2. The API exercise and fixed end-to-end test verify these cases.

**Limits:** No shared-role model, persistent storage, external identity provider or real deployment was evaluated.
