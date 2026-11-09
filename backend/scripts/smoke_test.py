import json,urllib.request
base='http://127.0.0.1:8000'
d=json.loads(urllib.request.urlopen(urllib.request.Request(base+'/api/v1/auth/login', data=b'{"email":"admin@edupredict.com","password":"admin123"}', headers={'Content-Type':'application/json'}),timeout=60).read())
h={'Authorization':'Bearer '+d['access_token']}
def get(u): return urllib.request.urlopen(urllib.request.Request(base+u,headers=h),timeout=180)
def post(u,b=b'{}'): return urllib.request.urlopen(urllib.request.Request(base+u,data=b,headers={**h,'Content-Type':'application/json'}),timeout=300)
print('health', urllib.request.urlopen(base+'/health').read().decode())
print('users', len(json.loads(get('/api/v1/users/').read())))
print('analytics', json.loads(get('/api/v1/analytics/summary').read()))
run=json.loads(post('/api/v1/predictions/run/2/week_4').read()); print('run', run.get('status'), run.get('model_name'), run.get('summary'))
ar=json.loads(get('/api/v1/predictions/at-risk?period_id=2&checkpoint=week_4&risk_band=high').read()); print('at_risk_high', len(ar))
rec=json.loads(get('/api/v1/recommendations/generated?period_id=2&checkpoint=week_4').read()); print('recommendations', rec.get('count'))
rep=json.loads(post('/api/v1/reports/generate', b'{"report_type":"course_risk","report_format":"excel","checkpoint":"week_4","period_id":2}').read()); print('report', rep.get('id'), rep.get('rows'))
print('OK')
