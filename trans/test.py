s = "hi"


tmp = s.split("\n")
result = []
idx = 0

for i in range(len(tmp)):
    tmp[i] = tmp[i].replace("\n", "")
    if (tmp[i][-1] == "." or tmp[i][-1] == "!" or tmp[i][-1] == "?"):
        try:
            print(ord(tmp[i+1][0]))
            boo = ord(tmp[i+1][0]) < 97
        except:
            boo = True
        if(boo):    
            res = ""
            while(idx <= i):
                res = res + " " + tmp[idx]
                idx += 1
            result.append(res)
        
print(result[0])    

