import os, boto3
from flask import Flask, render_template_string

TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'argus-incidents')

app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html><head>
<title>Argus Dashboard</title>
<style>
  body{font-family:Arial;margin:40px}
  table{border-collapse:collapse;width:100%}
  th,td{border:1px solid #ccc;padding:8px;text-align:left}
  th{background:#2E75B6;color:white}
  tr:nth-child(even){background:#f2f2f2}
</style>
</head><body>
<h1>Argus — Incident History</h1>
<table>
  <tr><th>Time</th><th>Alert</th><th>Severity</th><th>Playbook</th><th>Summary</th></tr>
  {% for i in incidents %}
  <tr>
    <td>{{i.get('timestamp','')}}</td>
    <td>{{i.get('alertname','')}}</td>
    <td>{{i.get('severity','')}}</td>
    <td>{{i.get('playbook','')}}</td>
    <td>{{i.get('postmortem_summary','')}}</td>
  </tr>
  {% endfor %}
</table>
</body></html>
'''

@app.route('/')
def index():
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table(TABLE_NAME)
    result   = table.scan(Limit=10)
    incidents = sorted(
        result.get('Items', []),
        key=lambda x: x.get('timestamp', ''),
        reverse=True
    )[:5]
    return render_template_string(HTML, incidents=incidents)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
