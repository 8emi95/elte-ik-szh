import sys

class HaziCRCCalculator(object):
    generator = '11011'

    def getRemainder(self, number, denominator):
        print "%s : %s" % (number, denominator)

        d_len = len(denominator)
        d = self.getAsInt(denominator)

        pos = d_len
        while len(number) >= d_len:
            numerator = self.getAsInt(number[:d_len])
            print ("{:>%d}" % (pos)).format(number[:d_len])
            print ("{:>%d}" % (pos)).format(denominator)
            print ("{:>%d}" % (pos)).format(("{:->%d}" % (d_len)).format(''))
            remainder = "{0:b}".format(numerator ^ d)
            pos += d_len - len(remainder)
            number = remainder + number[d_len:]
        print ("{:>%d}" % (pos)).format(number)        
        return "{0:b}".format(self.getAsInt(number))

    def getAsInt(self, binaryStr):
        return int(binaryStr, 2)
    
    def getWithCrc(self, number):
        remainder = self.getRemainder(number + ("{:0>%d}" % (len(self.generator) - 1)).format(''), self.generator)
        return number + ("{:0>%d}" % (len(self.generator) - 1)).format(remainder)
