import argparse
import json
import os
import sys

PLAYBOOK_MAP = {
    'PodCrashLooping': 'restart-deployment',
    'HighMemoryUsage': 'rollback-deployment',
    'HighCPU':         'scale-up',
}


def rule_based_classify(alert: dict) -> dict:
    alertname = alert.get('labels', {}).get('alertname', 'Unknown')
    severity  = alert.get('labels', {}).get('severity', 'warning')
    playbook  = PLAYBOOK_MAP.get(alertname, 'unknown')

    result = {
        'alertname': alertname,
        'severity':  severity,
        'playbook':  playbook,
        'source':    'rules',
    }

    # Optional AI enrichment — safe to skip if GROQ_API_KEY not set
    try:
        # Ensure scripts/ dir is on the path when run from the repo root
        scripts_dir = os.path.dirname(os.path.abspath(__file__))
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from ai_enrich import enrich_classification
        result = enrich_classification(result, alert)
    except Exception as e:
        result['ai_enrichment'] = f'skipped ({e})'

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--alert',  required=True, help='JSON string of the alert payload')
    parser.add_argument('--output', required=True, help='Path to write classification.json')
    args = parser.parse_args()

    try:
        alert = json.loads(args.alert)
    except json.JSONDecodeError as exc:
        print(f'ERROR: Invalid alert JSON — {exc}', file=sys.stderr)
        sys.exit(1)

    result = rule_based_classify(alert)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f'Classification written to {args.output}: alertname={result["alertname"]}, playbook={result["playbook"]}')
