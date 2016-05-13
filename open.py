

# def printShow(*value,ifprint = True,text = True,nobyte = True):
#     ''' print to CMD and text plain
#     '''
#     printlist = list()
#     textlist = list()
#     if value:
#         for x in value:
#             if type(x) == str:
#                 printlist.append(x)
#                 textlist.append(x)
#             elif type(x) == int:
#                 printlist.append(str(x))
#                 textlist.append(str(x))
#             elif type(x) == bytes:
#                 if nobyte == True:
#                     textlist.append(x.hex())
#                     # printlist.append(':'+str(x))
#                 elif nobyte == False:
#                     textlist.append(':'+str(x))
#                 printlist.append(':'+str(x))
#             else:
#                 printlist.append(str(x))
#                 textlist.append(str(x))
#         if ifprint:
#             print(''.join(printlist))
#         if text:
#             printText = ''.join(textlist)
#             if printText != ':bytes':
#                 pass
#                 # self.printText.put(printText)

c = b'\x01\x02\x03\xFF\xFE'
xhex = c.hex()
xlist = list()
t=0
for x in xhex:
    if t == 1:
        xlist.append(x+' ')
        t = 0
    else:
        xlist.append(x)
        t = t+1
    print(t)

xstr = ''.join(xlist)
print(xstr)


# printShow(x)
#

