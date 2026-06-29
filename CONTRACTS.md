# Argus Contracts - The 5 Binding Rules

**Everyone must follow these rules exactly.**

## Rule 1: Alert Webhook
Alertmanager POSTs to Jenkins. Jenkins extracts `$.alerts[0]` (the first alert only).

## Rule 2: classification.json
- Track B writes this file
- Track C only ADDS fields (never modifies existing ones)
- No one changes `playbook` or `severity` once set

## Rule 3: postmortem.json
Track C writes this after adding:
- `incident_id`
- `timestamp`
- AI summary

## Rule 4: AWS Names
Track A shares DynamoDB table name and S3 bucket name with Track C immediately after `terraform apply`.

## Rule 5: Playbook Naming
Every file in `ansible/playbooks/` must be registered in `PLAYBOOK_MAP` in `classify_incident.py`.

---

## Validation

```bash
python3 scripts/validate_contract.py classification classification.json
python3 scripts/validate_contract.py postmortem postmortem.json
