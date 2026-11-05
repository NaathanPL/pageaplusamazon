# usage: python3 show.py <tool-result.txt> <out.jpg> : écrit l'image B64 et affiche le reste du JSON
import sys,json,re,base64
t=json.load(open(sys.argv[1]))[0]['text']
m=re.search(r'B64START(.*?)B64END',t,re.S)
if m: open(sys.argv[2],'wb').write(base64.b64decode(m.group(1)))
t=re.sub(r'x{50,}B64START.*?B64END','<IMG>',t,flags=re.S)
print(t[:2500])
