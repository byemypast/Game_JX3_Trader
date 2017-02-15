import re
f = open("ah.jx3dat",'rb')
head = f.read(16)
msg = f.read().decode()
pattern2 = re.compile('\[(.*?)\]=\{\[1\]=\{\[\"nGold\"\]=(.*?),\[\"nSilver\"\]=(.*?),\[\"nCopper\"\]=(.*?),},\[2\]=(.*?),},')
print(msg)
print(pattern2.findall(msg))