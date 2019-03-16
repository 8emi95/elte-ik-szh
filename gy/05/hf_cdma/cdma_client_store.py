class CDMAClientStore(object):
    store = {
        '[0,0,0,1]': None,
        '[0,0,1,0]': None,
        '[0,1,0,0]': None,
        '[1,0,0,0]': None
    }

    def getClientHandlers(self):
        return list([v['socket'] for k,v in self.store.iteritems() if v is not None ])

    def getClientNames(self):
        return list([v['name'] for k,v in self.store.iteritems() if v is not None ])

    def getChips(self):
        return list([k for k,v in self.store.iteritems() ])

    def getClientNum(self):
        return len(list([v for k,v in self.store.iteritems() if v is not None ]))

    def getClientNameBySocket(self, socket):
        ret = [v['name'] for k,v in self.store.iteritems() if v is not None and v['socket'] == socket]
        return ret[0] if ret else ''

    def getClientSocketByName(self, name):
        ret = [v['socket'] for k,v in self.store.iteritems() if v is not None and v['name'] == name]
        return ret[0] if ret else None

    def getClientChipByName(self, name):
        ret = [k for k,v in self.store.iteritems() if v is not None and v['name'] == name]
        return ret[0] if ret else ''

    def addClient(self, name, socket):
        chip = self.getFirstEmptyChip()
        if chip:
            self.store[chip] = {
                'name': name,
                'socket': socket
            }
            return chip
        else:
            return 'NNNN'

    def remove(self, socket):
        name = self.getClientNameBySocket(socket)
        if name:
            self.store[self.getClientChipByName(name)] = None

    def getFirstEmptyChip(self):
        emptyChips = [k for k,v in self.store.iteritems() if v is None]
        return emptyChips[0] if emptyChips else None