import json,base64,sys
t=json.load(open(sys.argv[1]))[0]['text']; b=t.split('B64START')[1].split('B64END')[0]; open(sys.argv[2],'wb').write(base64.b64decode(b))
