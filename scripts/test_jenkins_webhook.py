import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_URL = 'http://localhost:8080/generic-webhook-trigger/invoke?token=argus-token'

SAMPLE_ALERT = {
    'alerts': [
        {
            'status': 'firing',
            'labels': {
                'alertname': 'PodCrashLooping',
                'severity': 'critical',
            },
            'annotations': {
                'summary': 'Test alert from Argus validation script.',
            },
        }
    ]
}


def main():
    parser = argparse.ArgumentParser(
        description='Send a sample Alertmanager webhook payload to Jenkins.'
    )
    parser.add_argument(
        '--url', default=DEFAULT_URL, help='Full Jenkins webhook URL'
    )
    args = parser.parse_args()

    payload = json.dumps(SAMPLE_ALERT).encode('utf-8')
    request = Request(
        args.url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urlopen(request, timeout=15) as response:
            body = response.read().decode('utf-8', errors='replace')
            print(f'Webhook response: {response.status} {response.reason}')
            if body:
                print(body)
    except HTTPError as exc:
        print(f'Webhook error: {exc.code} {exc.reason}')
        try:
            print(exc.read().decode('utf-8', errors='replace'))
        except Exception:
            pass
        sys.exit(1)
    except URLError as exc:
        print(f'Webhook connection failed: {exc}')
        sys.exit(1)


if __name__ == '__main__':
    main()
