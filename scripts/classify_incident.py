import argparse
import json
import os

PLAYBOOK_MAP = {
    'PodCrashLooping': 'restart-deployment',
    'HighMemoryUsage': 'rollback-deployment',
    'HighCPU': 'scale-up',
}

def rule_based_classify(alert: dict) -> dict:
    alertname = alert.get('labels', {}).get('alertname', 'Unknown')
    severity = alert.get('labels', {}).get('severity', 'warning')
    playbook = PLAYBOOK_MAP.get(alertname, 'unknown')

    result = {
        'alertname': alertname,
        'severity': severity,
        'playbook': playbook,
        'source': 'rules',
    }

    # Optional AI enrichment (safe to skip if key not set)
    try:
        from ai_enrich import enrich_classification
        result = enrich_classification(result, alert)
    except Exception as e:
        result['ai_enrichment'] = f'skipped ({e})'

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--alert', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    alert = json.loads(args.alert)
    result = rule_based_classify(alert)

    with open(args.output, 'w') as f:
        json.dump(result, f)

    print(f'Classification written to {args.output}')
