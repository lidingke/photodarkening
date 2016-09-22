from slave.source import Source
from slave.pump import Pump
import threading



class Mainthread(threading.Thread):
    """docstring for Mainthread"""
    def __init__(self, ):
        super(Mainthread, self).__init__()
        # self.arg = arg

    def run(self):
        s = Source()
        p = Pump()
        s.start()
        p.start()
        while True:
            try:
                pass
            except KeyboardError:
                return



if __name__ == '__main__':
    # threading.Thread(target=mainthread ).start()
    m = Mainthread()
    m.start()

