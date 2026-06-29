import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, render_template_string

TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'argus-incidents')

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="15">
  <title>Argus Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
    h1   { color: #2E75B6; }
    table{ border-collapse: collapse; width: 100%; background: white; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
    th   { background: #2E75B6; color: white; }
    tr:nth-child(even) { background: #f2f2f2; }
    .note  { margin-bottom: 12px; color: #555; font-size: 0.9em; }
    .error { color: #c0392b; background: #fdecea; padding: 10px; border-radius: 4px; }
    .empty { color: #888; font-style: italic; }
  </style>
</head>
<body>
  <h1>Argus — Incident History</h1>
  <p class="note">Showing the 10 most recent incidents. Page refreshes every 15 seconds.</p>
  {% if error %}
    <p class="error">⚠ Could not load incidents: {{ error }}</p>
  {% elif not incidents %}
    <p class="empty">No incidents recorded yet.</p>
  {% else %}
  <table>
    <tr><th>Time (UTC)</th><th>Alert</th><th>Severity</th><th>Playbook</th><th>Summary</th></tr>
    {% for i in incidents %}
    <tr>
      <td>{{ i.get('timestamp', '') }}</td>
      <td>{{ i.get('alertname', '') }}</td>
      <td>{{ i.get('severity', '') }}</td>
      <td>{{ i.get('playbook', '') }}</td>
      <td>{{ i.get('postmortem_summary', '') }}</td>
    </tr>
    {% endfor %}
  </table>
  {% endif %}
</body>
</html>
'''


@app.route('/')
def index():
    error     = None
    incidents = []
    try:
        dynamodb = boto3.resource('dynamodb')
        table    = dynamodb.Table(TABLE_NAME)
        # Scan in pages and collect up to 100 items, then return the newest 10.
        paginator = dynamodb.meta.client.get_paginator('scan')
        items = []
        for page in paginator.paginate(TableName=TABLE_NAME, PaginationConfig={'MaxItems': 100}):
            items.extend(page.get('Items', []))
        incidents = sorted(items, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
    except (BotoCoreError, ClientError) as exc:
        error = str(exc)

    return render_template_string(HTML, incidents=incidents, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
