with open('data\\1.txt','w') as f:
    st = 'hello file'
    f.write(st)

with open('data\\1.txt','rb') as f:
    a = f.readlines()
    print(a)


