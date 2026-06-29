import argparse, json, os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('GROQ_API_KEY', ''),
    base_url='https://api.groq.com/openai/v1',
)

FALLBACK = (
    'Incident: {alertname} (severity: {severity}). '
    "Remediation playbook '{playbook}' was executed automatically. "
    'AI summary unavailable — check classification.json for details.'
)

def generate(classification: dict) -> str:
    prompt = f'''Write a 3-sentence incident postmortem for an SRE Slack channel. Be specific and plain-English, no jargon.
Data: {json.dumps(classification)}'''
    try:
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return FALLBACK.format(**classification)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classification', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    with open(args.classification) as f:
        classification = json.load(f)

    classification['postmortem_summary'] = generate(classification)

    with open(args.output, 'w') as f:
        json.dump(classification, f, indent=2)

    print('Postmortem written to', args.output)
