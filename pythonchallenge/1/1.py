# http://www.pythonchallenge.com/pc/def/map.html

q = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
q.replace(' ', '')
q = list(q)
print(q)
ans = []
print("Q: ", q)

for i in range(len(q)):
    ans.append(chr(ord(q[i])+2))

print(''.join(ans))

# http://www.pythonchallenge.com/pc/def/ocr.html