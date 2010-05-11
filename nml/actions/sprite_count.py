from nml.generic import *

class SpriteCountAction:
    def __init__(self, count):
        self.count = count
    
    def prepare_output(self):
        pass
    
    def write(self, file):
        file.print_decimal(4, 2)
        file.print_dword(self.count)
        file.newline()
        file.newline()
