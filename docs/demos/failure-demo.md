# Failure Demo

## Purpose

This document describes a simple local demo for showing degraded behavior without breaking the full workflow. The goal is to demonstrate that deterministic contradiction logic still works when the assistive contradiction-analysis prompt is unavailable.

## Demo objective

Show that the system can:

- enter degraded mode truthfully
- still create deterministic findings
- still attach citations
- still create review tasks
- still record observability output

## Preconditions

Before starting, ensure:

- PostgreSQL and Redis are running
- migrations are applied
- seed data is loaded
- backend server is running
- Celery worker is running

## Baseline state

The normal seeded state includes an active contradiction-analysis prompt version. In this state, comparison runs complete normally and model execution logs show assistive success.

## Step 1: disable contradiction-analysis prompt

Run from path: `D:\AI-Projects\agentic-compliance-auditor\backend`

Virtual environment required: yes

```powershell
cd D:\AI-Projects\agentic-compliance-auditor\backend
.\.venv\Scripts\activate
python manage.py shell
````

Inside the Django shell:

```python
from apps.observability.models import PromptVersion
PromptVersion.objects.filter(purpose="contradiction_analysis").update(is_active=False)
exit()
```

Expected interpretation:

* the contradiction-analysis prompt is now inactive
* future comparison runs should fall back to deterministic rules and mark the run as degraded

## Step 2: launch a comparison run

Use either the UI or API to trigger a comparison run against the known seeded contradiction pair.

Recommended seeded pair:

* source: `Complaints Escalation Policy v3`
* target: `Complaints Control Standard v5`

A new comparison run should still create a timeline-conflict finding.

Expected interpretation:

* the comparison completes with degraded status
* citations are still present
* a review task is still created
* observability should show fallback usage rather than assistive success

## Step 3: inspect outputs

Inspect the following areas:

* findings dashboard
* finding detail page
* review queue
* metrics endpoints
* comparison-run API response
* model execution log records in admin if needed

You should be able to show that the workflow degraded honestly without disappearing.

## Step 4: re-enable contradiction-analysis prompt

Run from path: `D:\AI-Projects\agentic-compliance-auditor\backend`

Virtual environment required: yes

```powershell
cd D:\AI-Projects\agentic-compliance-auditor\backend
.\.venv\Scripts\activate
python manage.py shell
```

Inside the Django shell:

```python
from apps.observability.models import PromptVersion
PromptVersion.objects.filter(name="contradiction-analysis-default").update(is_active=True)
exit()
```

Expected interpretation:

* the default contradiction-analysis prompt is active again
* future comparison runs return to normal assistive status

## What this demo proves

This demo proves the following design claims:

* deterministic rules remain authoritative
* assistive AI is not the sole workflow dependency
* degraded mode is explicit rather than hidden
* findings still remain evidence-backed
* review routing continues under degraded conditions

## What this demo does not prove

This demo does not claim:

* production-grade resilience
* full semantic contradiction coverage
* zero operational risk under dependency failure
* legal or regulatory interpretation accuracy

## Summary

The failure demo is a controlled degraded-mode walkthrough. It shows that the system can continue producing auditable, reviewable contradiction findings even when assistive contradiction prompting is unavailable.