from slave.source import Source
from slave.pump import Pump

if __name__ == '__main__':
    s = Source()
    p = Pump()

    s.start()
    p.start()
