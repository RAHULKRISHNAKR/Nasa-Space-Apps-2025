import json
from src.api import app
from fastapi.testclient import TestClient
c = TestClient(app)
r = c.post('/forecast', json={'lat':10.0891,'lon':76.5994,'hours':6})
print('status', r.status_code)
print('json', r.json())
with open('demo_output.json','w') as f:
    json.dump({'forecast_response': r.json()}, f, indent=2)
