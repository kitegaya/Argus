import json
import os


def _get_client():
    """Lazy-init the Groq/OpenAI client — avoids crash when key is absent."""
    api_key = os.environ.get('GROQ_API_KEY', '')
    if not api_key:
        raise EnvironmentError('GROQ_API_KEY is not set')
    from openai import OpenAI
    return OpenAI(
        api_key=api_key,
        base_url='https://api.groq.com/openai/v1',
    )


def enrich_classification(rule_result: dict, alert: dict) -> dict:
    prompt = (
        'You are an SRE assistant. Given this alert and rule-based classification, '
        'suggest a likely root cause in one sentence.\n'
        f'Alert: {json.dumps(alert)}\n'
        f'Rule classification: {json.dumps(rule_result)}\n'
        'Respond with JSON only, no extra text: {"likely_cause": "..."}'
    )

    try:
        client   = _get_client()
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=150,
        )
        raw        = response.choices[0].message.content.strip()
        enrichment = json.loads(raw)
        rule_result['likely_cause']  = enrichment['likely_cause']
        rule_result['ai_enrichment'] = 'groq'
    except Exception as e:
        rule_result['likely_cause']  = 'AI enrichment unavailable'
        rule_result['ai_enrichment'] = f'skipped ({e})'

    return rule_result
