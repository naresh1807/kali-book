# Security curriculum: serial study checklist

Read the new security curriculum in the website Start here page. Complete steps 01–18 in order; retain the existing 45-chapter reference for tool details. Begin with computer/network foundations if those are new to you.

- [ ] 01. Security goals and trust boundaries (Beginner)
  Practice: For a fictional student portal, mark private grades, authorized grade changes and required availability. Draw browser, application and database boundaries.
- [ ] 02. Assets, threats, vulnerabilities and risk (Beginner)
  Practice: Write one scenario with asset, threat action, weakness, impact, control and residual uncertainty. Compare an internal test page with a customer-facing payment service.
- [ ] 03. Threat modeling and misuse cases (Beginner)
  Practice: Draw a synthetic invoice download flow. Add an unauthorized reader and identify where ownership should be enforced. Link the model to the two-account API case study.
- [ ] 04. Hashing, encryption, signatures and password storage (Beginner to intermediate)
  Practice: Classify four tasks: compare file copies, protect stored records, verify a software publisher and check a password. Explain why each needs a different mechanism.
- [ ] 05. Certificates, PKI and secure transport (Intermediate)
  Practice: Use the existing TLS worksheet to record expected hostname, trust roots and failure behavior. Explain why disabling certificate validation hides a problem.
- [ ] 06. Identity, authorization and least privilege (Intermediate)
  Practice: Create a role-by-resource matrix with owner, another user and administrator. Include an allowed action and a denied action for each supported role.
- [ ] 07. Secrets lifecycle and credential exposure (Intermediate)
  Practice: Write a fictional leaked-token response plan: revoke it, determine exposure, replace dependent configuration, validate access and investigate the leak source.
- [ ] 08. Endpoint hardening and patch management (Intermediate)
  Practice: Create a baseline for a disposable VM: required services, account privileges, update state, firewall policy and rollback method. Compare intended with observed settings.
- [ ] 09. Backups, resilience and restoration (Intermediate)
  Practice: Use synthetic files to document a backup and restore exercise. Verify contents, permissions and the recovery steps rather than only checking that a backup file exists.
- [ ] 10. Data classification, minimization and retention (Intermediate)
  Practice: Inventory synthetic customer fields and decide which are needed for a feature. Create a redacted report that preserves evidence without exposing reusable credentials.
- [ ] 11. Cloud shared responsibility and IAM (Intermediate to advanced)
  Practice: For a fictional storage service, map who manages the platform, who grants access and who controls the data. Test one intended reader and one denied reader in a separately configured lab.
- [ ] 12. Container isolation and workload security (Intermediate to advanced)
  Practice: Review a fictional deployment manifest for unnecessary privileges and secret placement. Explain which settings affect the host and which affect only the application.
- [ ] 13. Software supply chain and secure delivery (Advanced)
  Practice: Trace a fictional commit through build and deployment. Mark who may change code, read secrets, approve a release and publish an artifact.
- [ ] 14. Security logging and observability (Advanced)
  Practice: Create an event schema for a denied profile update: time, synthetic actor ID, operation, resource label, result and correlation ID. Explain what must be redacted.
- [ ] 15. Detection validation and security metrics (Advanced)
  Practice: Use the network attack scenarios to compare gateway failover with suspicious mapping changes. State the extra evidence needed before escalation.
- [ ] 16. Incident response and recovery decisions (Advanced)
  Practice: Run a tabletop for a synthetic exposed service token. Record who revokes it, checks affected actions, repairs the leak and verifies restored operation.
- [ ] 17. Governance, risk ownership and control evidence (Advanced)
  Practice: Assign an owner, objective, validation method and review date to three fictional controls. Record who accepts a residual risk and why.
- [ ] 18. Integrated security assessment and retest (Advanced capstone)
  Practice: Produce a short report with confirmed finding, root cause, remediation, retest and remaining limitations. Link each assertion to a specific fixture or observation.

For each step, record: explanation in your own words, synthetic example, evidence, common mistake, answer to the self-check and remaining questions.

Capstone: use the supplied advanced-casebook lab and report template; run its documented fixed/vulnerable comparisons. No new remote targets, accounts or services are created by this checklist.

References: [NIST CSF 2.0](https://www.nist.gov/cyberframework), [OWASP secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
