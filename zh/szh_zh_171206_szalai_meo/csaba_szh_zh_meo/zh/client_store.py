class ClientStore(object):
    store = {}

    def getClientHandlers(self):
        return list([k for k,v in self.store.iteritems()])

    def getClientNames(self):
        return list([v for k,v in self.store.iteritems()])
    
    def getClientNameBySocket(self, socket):
        ret = [v for k,v in self.store.iteritems() if v is not None and k == socket]
        return ret[0] if ret else ''

    def getClientSocketByName(self, name):
        ret = [k for k,v in self.store.iteritems() if v is not None and v == name]
        return ret[0] if ret else None

    def addClient(self, name, socket):
            self.store[socket] = name

    def remove(self, socket):
        if store[socket] is not None:
            del store[socket]