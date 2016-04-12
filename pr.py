import pdb

def pr(*value):
    b = list()
    if value:
        # print(len(value))
        for x in value:
            # print(type(x))
            if type(x) == int:
                # pdb.set_trace()
                b.append(str(x))
            elif type(x) == bytes:
                hhex = '%02x'%ord(x)
                b.append('/'+str(hhex))
            else:
                b.append(str(x))
        c = ''.join(b)
        # print(value)
        # pdb.set_trace()
        print(c)


pr('a',19,2,b'\x09\xFF')
