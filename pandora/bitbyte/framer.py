class Framer(object):
    codebook = {
        'FLAG':'01111110', 
        'A':'10000001', 
        'B':'00001110',
        'C':'10110011', 
        'D':'11100110', 
        'ESC':'01110000'
    }

    def frame(self, msg, mode):
        if mode == 'bit':
            return self.frameBitMode(msg)
        elif mode == 'byte':
            return self.frameByteMode(msg)

    def getMsgValue(self, msg):
        return ''.join([self.codebook[m] for m in msg.split(',')])

    def frameBitMode(self, msg):
        return self.codebook['FLAG'] + self.getMsgValue(msg).replace('11111', '111110') + self.codebook['FLAG']

    def frameByteMode(self, msg):
        escaped = self.getMsgValue(msg).replace(self.codebook['ESC'], self.codebook['ESC'] + self.codebook['ESC'])
        escaped = escaped.replace(self.codebook['FLAG'], self.codebook['ESC'] + self.codebook['FLAG'])
        return self.codebook['FLAG'] + escaped + self.codebook['FLAG']

    def getValueFromMsg(self, msg):
        for key, value in self.codebook.iteritems():
            msg = msg.replace(value, key + ',')
        return msg[:-1]

    def unframe(self, msg, mode):
        if mode == 'bit':
            return self.getValueFromMsg(self.unframeBitMode(msg))
        elif mode == 'byte':
            return self.getValueFromMsg(self.unframeByteMode(msg))

    def unframeBitMode(self, msg):
        flag_length = len(self.codebook['FLAG'])
        return msg[flag_length : -flag_length].replace('111110', '11111')
    
    def unframeByteMode(self, msg):
        flag_length = len(self.codebook['FLAG'])
        msg = msg[flag_length : -flag_length]
        msg = msg.replace(self.codebook['ESC'] + self.codebook['ESC'], self.codebook['ESC'])
        msg = msg.replace(self.codebook['ESC'] + self.codebook['FLAG'], self.codebook['FLAG'])
        return msg