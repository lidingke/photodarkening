from modelpump import TempDetector

t = 1.9#*10**-3
temp = TempDetector()

power = temp.getPower(22.4,t)
print(power)
