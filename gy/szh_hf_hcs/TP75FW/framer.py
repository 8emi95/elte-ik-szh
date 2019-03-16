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
            return self.frame_bit_mode(msg)
        else:
            return self.frame_byte_mode(msg)

    def _get_msg_value(self, msg):
        return ''.join([self.codebook[m] for m in msg.split(',')])

    def frame_bit_mode(self, msg):
        return self.codebook['FLAG'] + self._get_msg_value(msg).replace('11111', '111110') + self.codebook['FLAG']

    def frame_byte_mode(self, msg):
        escaped = self._get_msg_value(msg).replace(self.codebook['ESC'], self.codebook['ESC'] + self.codebook['ESC'])
        escaped = escaped.replace(self.codebook['FLAG'], self.codebook['ESC'] + self.codebook['FLAG'])
        return self.codebook['FLAG'] + escaped + self.codebook['FLAG']

    def unframe(self, msg, mode):
        if mode == 'bit':
            return self._get_value_from_msg(self.unframe_bit_mode(msg))
        else:
            return self._get_value_from_msg(self.unframe_byte_mode(msg))

    def unframe_bit_mode(self, msg):
        flag_length = len(self.codebook['FLAG'])
        return msg[flag_length : -flag_length].replace('111110', '11111')
    
    def unframe_byte_mode(self, msg):
        flag_length = len(self.codebook['FLAG'])
        msg = msg[flag_length : -flag_length]
        msg = msg.replace(self.codebook['ESC'] + self.codebook['ESC'], self.codebook['ESC'])
        msg = msg.replace(self.codebook['ESC'] + self.codebook['FLAG'], self.codebook['FLAG'])
        return msg

    def _get_value_from_msg(self, msg):
        for key, value in self.codebook.iteritems():
            msg = msg.replace(value, key + ',')
        return msg