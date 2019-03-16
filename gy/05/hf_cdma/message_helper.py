from collections import deque

class MessageHelper(object):
    """ The message interferer """
    def interfere(self, msg1, msg2):
        interfered = deque()
        msg1 = self.getMsgAsDeque(msg1)
        msg2 = self.getMsgAsDeque(msg2)
        while msg1 and msg2:
            interfered.appendleft([a+b for a,b in zip(msg1.pop(), msg2.pop())])
        while msg1:
            interfered.appendleft(msg1.pop())
        while msg2:
            interfered.appendleft(msg2.pop())
        return '[' + ','.join([str(v) for v in interfered]) + ']'

    def getMsgAsDeque(self, msg):
        return deque(map(lambda x: [int(val) for val in x.split(',')], msg[2:-2].split('],[')))