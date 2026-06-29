"""
Argus contract validator — verifies that classification.json and
postmortem.json conform to the schemas defined in CONTRACTS.md.

Usage:
    python3 scripts/validate_contract.py classification classification.json
    python3 scripts/validate_contract.py postmortem postmortem.json
"""

import argparse
import json
import sys

# ── Schemas ────────────────────────────────────────────────────────────────────
SCHEMAS = {
    'classification': {
        'required': ['alertname', 'severity', 'playbook', 'source'],
        'types': {
            'alertname': str,
            'severity':  str,
            'playbook':  str,
            'source':    str,
        },
        'immutable_after_track_b': ['playbook', 'severity'],
    },
    'postmortem': {
        'required': [
            'alertname', 'severity', 'playbook', 'source',
            'incident_id', 'timestamp', 'postmortem_summary',
        ],
        'types': {
            'alertname':         str,
            'severity':          str,
            'playbook':          str,
            'source':            str,
            'incident_id':       str,
            'timestamp':         str,
            'postmortem_summary': str,
        },
    },
}


def validate(schema_name: str, data: dict) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    schema = SCHEMAS.get(schema_name)
    if schema is None:
        return [f'Unknown schema: {schema_name!r}. Choose from: {list(SCHEMAS)}']

    errors = []

    for field in schema['required']:
        if field not in data:
            errors.append(f'Missing required field: {field!r}')

    for field, expected_type in schema.get('types', {}).items():
        if field in data and not isinstance(data[field], expected_type):
            errors.append(
                f'Field {field!r} must be {expected_type.__name__}, '
                f'got {type(data[field]).__name__}'
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate an Argus contract JSON file.')
    parser.add_argument('schema',  choices=list(SCHEMAS), help='Schema to validate against')
    parser.add_argument('file',    help='Path to the JSON file to validate')
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f'ERROR: File not found: {args.file}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f'ERROR: Invalid JSON in {args.file}: {exc}', file=sys.stderr)
        sys.exit(1)

    errors = validate(args.schema, data)
    if errors:
        print(f'Contract validation FAILED for {args.file!r} ({args.schema} schema):')
        for err in errors:
            print(f'  ✗ {err}')
        sys.exit(1)

    print(f'Contract validation PASSED for {args.file!r} ({args.schema} schema).')


if __name__ == '__main__':
    main()
