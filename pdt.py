# from modelpump import TempDetector

def getPower(temp = 0, voltage = 0,):
    para = {
    'B01-SMC': [20,50.3,0.088],
    'B05-SMC': [20,134.2,0.235],
    'C50-MC':   [20,0.59775,0.000747]
    }
    getpara = para['C50-MC']
    stand_temp = getpara[0]
    init_sen = getpara[1]
    correct_sen = getpara[2]
    #Z=Z0+（T-T0）*Zc
    sensitivity = init_sen +(temp-stand_temp)*correct_sen
    #Φ = U/Z
    voltage = (voltage*1000-8.977)/346.34
    power = voltage/sensitivity

    return power
    # print('power:',power)

t = 1.9#*10**-3
listtt = [
0.15,
0.27,
0.39,
0.51,
0.63,
0.74,
0.85,
0.99,
1.12,
1.24,
1.34,
1.45,
1.56,
1.67,
1.79,
1.91,
2.03,
]
# temp = TempDetector()
for x in listtt:
    pass
    power = getPower(23.4,x)
    print(power)

