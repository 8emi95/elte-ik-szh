import re

class Crypt(object):
    dataSymbols = re.compile(r"[01]")
    dropSymbols = re.compile(r"[[\](){} ]", re.IGNORECASE)
    
    def encrypt(self, chip, data):
        chip = self.getVectFromChip(chip)
        nchip = [x*(-1) for x in chip]
        self.__checkData(data)
        encrypted = [chip if bit == '1' else nchip for bit in data]
        ret = '[' + ','.join([str(v) for v in encrypted]) + ']'
        return ret

    def decrypt(self, chip, msg):
        chip = self.getVectFromChip(chip)
        msg = list(map(lambda x: [int(val) for val in x.split(',')], msg[2:-2].split('],[')))
        decrypted = []
        for val in msg:
            decrypted.append(reduce((lambda a,b: a+b), [x*y for x,y in zip(chip,val)]))
        ret = ''
        for val in decrypted:
            if val > 0:
                ret += '1'
            elif val == 0:
                ret += 'N'
            else:
                ret += '0'
        return ret

    def getVectFromChip(self, chip):
        return [int(x) for x in re.sub(self.dropSymbols, '', chip).split(',')]
    
    def __checkData(self, data):
        if len(re.sub(self.dataSymbols, '', data)) != 0:
            raise ValueError('Invalid data')