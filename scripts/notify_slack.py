import argparse
import json
import os
import sys

import requests

WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', '')


def notify(postmortem: dict) -> None:
    if not WEBHOOK_URL:
        print('SLACK_WEBHOOK_URL is not set — skipping Slack notification.')
        return

    text = (
        f"*Incident: {postmortem['alertname']}* "
        f"(severity: {postmortem['severity']})\n"
        f"Playbook run: `{postmortem['playbook']}`\n"
        f"{postmortem.get('postmortem_summary', 'No summary available.')}"
    )
    response = requests.post(WEBHOOK_URL, json={'text': text}, timeout=10)
    if response.status_code == 200:
        print('Slack notification sent.')
    else:
        print(f'Slack error: {response.status_code} {response.text}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--postmortem', required=True)
    args = parser.parse_args()

    with open(args.postmortem) as f:
        postmortem = json.load(f)

    notify(postmortem)
