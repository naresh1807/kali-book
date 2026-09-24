# Threat model worksheet

Target: synthetic localhost casebook app

## Data flow

Users / callback sender -> HTTP boundary -> Session and permission decisions -> In-memory invoice, profile, coupon and event state -> Redacted audit entries

## Fill in

| Asset | Actor | Entry point | Boundary | Abuse case | Control | Test | Owner | Gap |
|---|---|---|---|---|---|---|---|---|
| Invoice | Alice/Bob | GET invoice | Client/API | Cross-user read | Owner + tenant | API exercise | Learner | No shared roles |

Record assumptions, severity reasoning and the date you will review each decision. Compare the model with the actual code; update it when you add a new route.
