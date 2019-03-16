class Logger(object):
    def __init__(self, makeLog):
        self.makeLog = makeLog

    def log(self, *args):
        if self.makeLog:
            print ' '.join(args)

    def enableLogging(self):
        self.makeLog = True

    def disableLogging(self):
        self.makeLog = False        
