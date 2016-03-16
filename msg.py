msg = {
    'openseed':b' EB 90 01 00 00 01 90 EB',
    'openseedreturn':b' EB 90 01 00 00 01 90 EB',
    'openseederror':b' EB 90 01 00 10 00 90 EB',
    'closeseed':b' EB 90 01 00 00 00 90 EB',
    'closeseedreturn':b' EB 90 01 00 01 00 90 EB',
    'seedcurrentvalueset':b' EB 90 01 01 XX XX 90 EB',
    'seedcurrentvaluesetreturn':b' EB 90 01 01 XX XX 90 EB',
    'seedcurrentvalueseterror':b' EB 90 01 01 10 00 90 EB',
    'seedpulseset':b' EB 90 01 02 XX XX 90 EB',
    'seedpulsesetreturn':b' EB 90 01 02 XX XX 90 EB',
    'seedpulseseterror':b' EB 90 01 02 10 00 90 EB',
    'seedfreset':b' EB 90 01 03 XX XX 90 EB',
    'seedfresetreturn':b' EB 90 01 03 XX XX 90 EB',
    'seedfreseterror':b' EB 90 01 03 1000 90 EB',
    'seedcurrentvalueget':b' EB 90 01 04 90 EB',
    'seedcurrentvaluegetreturn':b' EB 90 01 04 XX XX 90 EB',
    'seedcurrentvaluegeterror':b' EB 90 01 04 10 00 90 EB',
    'seedpluseead':b' EB 90 01 05 90 EB',
    'seedplusereadreturn':b' EB 90 01 05 XX XX 90 EB',
    'seedplusereaderror':b' EB 90 01 05 10 00 90 EB',
    'seedfreread':b' EB 90 01 06 90 EB',
    'seedfrereadreturn':b' EB 90 01 06 XX XX 90 EB',
    'seedfrereaderror':b' EB 90 01 06 10 00 90 EB'
}

msg={'seedcurrentvalueset': b'\xEB\x90\x01\x01\xFF\xFF\x90\xEB',
'seedfresetreturn': b'\xEB\x90\x01\x03\xFF\xFF\x90\xEB',
'seedplusereadreturn': b'\xEB\x90\x01\x05\xFF\xFF\x90\xEB',
'seedfreseterror': b'\xEB\x90\x01\x03\x10\x00\x90\xEB',
'seedpluseead': b'\xEB\x90\x01\x05\x90\xEB',
'seedfrereaderror': b'\xEB\x90\x01\x06\x10\x00\x90\xEB',
'seedpulseset': b'\xEB\x90\x01\x02\xFF\xFF\x90\xEB',
'seedpulseseterror': b'\xEB\x90\x01\x02\x10\x00\x90\xEB',
'seedfrereadreturn': b'\xEB\x90\x01\x06\xFF\xFF\x90\xEB',
'closeseedreturn': b'\xEB\x90\x01\x00\x01\x00\x90\xEB',
'seedpulsesetreturn': b'\xEB\x90\x01\x02\xFF\xFF\x90\xEB',
'seedplusereaderror': b'\xEB\x90\x01\x05\x10\x00\x90\xEB',
'seedcurrentvaluesetreturn': b'\xEB\x90\x01\x01\xFF\xFF\x90\xEB',
'seedcurrentvalueseterror': b'\xEB\x90\x01\x01\x10\x00\x90\xEB',
'seedcurrentvalueget': b'\xEB\x90\x01\x04\x90\xEB',
'seedcurrentvaluegeterror': b'\xEB\x90\x01\x04\x10\x00\x90\xEB',
'openseederror': b'\xEB\x90\x01\x00\x10\x00\x90\xEB',
'seedfreread': b'\xEB\x90\x01\x06\x90\xEB',
'openseed': b'\xEB\x90\x01\x00\x00\x01\x90\xEB',
'openseedreturn': b'\xEB\x90\x01\x00\x00\x01\x90\xEB',
'closeseed': b'\xEB\x90\x01\x00\x00\x00\x90\xEB',
'seedcurrentvaluegetreturn': b'\xEB\x90\x01\x04\xFF\xFF\x90\xEB',
'seedfreset': b'\xEB\x90\x01\x03\xFF\xFF\x90\xEB'
}

#for k,v in msg.items():
#    msg[k] = v.replace(b" ",b"\x")
print(msg)
