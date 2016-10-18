from slave.slavex import SlaveX




if __name__ == '__main__':
    s = SlaveX()
    print ('getattr', s.run)
    s.start()
