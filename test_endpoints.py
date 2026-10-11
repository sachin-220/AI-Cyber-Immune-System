import requests

# Login first
login_resp = requests.post('http://localhost:8000/login', data={'company': 'DemoCompany'})
print('Login status:', login_resp.status_code)
print('Login response:', login_resp.text)

# Upload file for analysis
files = {'file': open('sample_security_data.csv', 'rb')}
r = requests.post('http://localhost:8000/analyze', files=files)
print('Analysis status:', r.status_code)
print('Analysis response:', r.text[:500])

# Get blockchain ledger
r = requests.get('http://localhost:8000/blockchain')
ledger = r.json()['ledger']
print('Blockchain Ledger (last 3 entries):')
for entry in ledger[-3:]:
    print('Hash:', entry['hash'][:20] + '...')
    print('Timestamp:', entry['timestamp'])
    print('Metadata:', entry['metadata'])
    print()