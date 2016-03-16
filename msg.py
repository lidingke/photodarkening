from collections import OrderedDict
msg = OrderedDict()

msg = {
        #open seed \x00
        'openseed':' EB 90 01 00 00 01 90 EB',
        'openseedreturn':' EB 90 01 00 00 01 90 EB',
        'openseederror':' EB 90 01 00 10 00 90 EB',
        #close seed \x00
        'closeseed':' EB 90 01 00 00 00 90 EB',
        'closeseedreturn':' EB 90 01 00 01 00 90 EB',
        # seed current \x01
        'seedcurrentvalueset':' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvaluesetreturn':' EB 90 01 01 FF FF 90 EB',
        'seedcurrentvalueseterror':' EB 90 01 01 10 00 90 EB',
        # seed pulse \x02
        'seedpulseset':' EB 90 01 02 FF FF 90 EB',
        'seedpulsesetreturn':' EB 90 01 02 FF FF 90 EB',
        'seedpulseseterror':' EB 90 01 02 10 00 90 EB',
        # seed fre \x03
        'seedfreset':' EB 90 01 03 FF FF 90 EB',
        'seedfresetreturn':' EB 90 01 03 FF FF 90 EB',
        'seedfreseterror':' EB 90 01 03 1000 90 EB',
        #seed current \x04
        'seedcurrentvalueget':' EB 90 01 04 90 EB',
        'seedcurrentvaluegetreturn':' EB 90 01 04 FF FF 90 EB',
        'seedcurrentvaluegeterror':' EB 90 01 04 10 00 90 EB',
        #seed pluse \x05
        'seedpluseread':' EB 90 01 05 90 EB',
        'seedplusereadreturn':' EB 90 01 05 FF FF 90 EB',
        'seedplusereaderror':' EB 90 01 05 10 00 90 EB',
        #seed frequance \x06
        'seedfreread':' EB 90 01 06 90 EB',
        'seedfrereadreturn':' EB 90 01 06 FF FF 90 EB',
        'seedfrereaderror':' EB 90 01 06 10 00 90 EB'
}

# msg={'seedcurrentvalueset': '\xEB\x90\x01\x01\xFF\xFF\x90\xEB',
# 'seedfresetreturn': '\xEB\x90\x01\x03\xFF\xFF\x90\xEB',
# 'seedplusereadreturn': '\xEB\x90\x01\x05\xFF\xFF\x90\xEB',
# 'seedfreseterror': '\xEB\x90\x01\x03\x10\x00\x90\xEB',
# 'seedpluseead': '\xEB\x90\x01\x05\x90\xEB',
# 'seedfrereaderror': '\xEB\x90\x01\x06\x10\x00\x90\xEB',
# 'seedpulseset': '\xEB\x90\x01\x02\xFF\xFF\x90\xEB',
# 'seedpulseseterror': '\xEB\x90\x01\x02\x10\x00\x90\xEB',
# 'seedfrereadreturn': '\xEB\x90\x01\x06\xFF\xFF\x90\xEB',
# 'closeseedreturn': '\xEB\x90\x01\x00\x01\x00\x90\xEB',
# 'seedpulsesetreturn': '\xEB\x90\x01\x02\xFF\xFF\x90\xEB',
# 'seedplusereaderror': '\xEB\x90\x01\x05\x10\x00\x90\xEB',
# 'seedcurrentvaluesetreturn': '\xEB\x90\x01\x01\xFF\xFF\x90\xEB',
# 'seedcurrentvalueseterror': '\xEB\x90\x01\x01\x10\x00\x90\xEB',
# 'seedcurrentvalueget': '\xEB\x90\x01\x04\x90\xEB',
# 'seedcurrentvaluegeterror': '\xEB\x90\x01\x04\x10\x00\x90\xEB',
# 'openseederror': '\xEB\x90\x01\x00\x10\x00\x90\xEB',
# 'seedfreread': '\xEB\x90\x01\x06\x90\xEB',
# 'openseed': '\xEB\x90\x01\x00\x00\x01\x90\xEB',
# 'openseedreturn': '\xEB\x90\x01\x00\x00\x01\x90\xEB',
# 'closeseed': '\xEB\x90\x01\x00\x00\x00\x90\xEB',
# 'seedcurrentvaluegetreturn': '\xEB\x90\x01\x04\xFF\xFF\x90\xEB',
# 'seedfreset': '\xEB\x90\x01\x03\xFF\xFF\x90\xEB'
# }

for k,v in msg.items():
    msg[k] = b''.fromhex(v) #v.replace(b" ",b"\x")
print(msg)
