# usage: python3 dec2.py <tool-result.txt> <out.jpg>
import sys,base64
t=open(sys.argv[1]).read(); i=t.find('B64START')+8; j=t.find('B64END',i)
open(sys.argv[2],'wb').write(base64.b64decode(t[i:j]))
