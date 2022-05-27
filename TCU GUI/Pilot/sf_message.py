import ctypes
from ctypes import Structure


class SFMessage(Structure):
    _fields_ = [
        ('flags', ctypes.c_uint8),
        ('switches', ctypes.c_uint8),
        ('vdir', ctypes.c_uint8),
        ('vspeed', ctypes.c_int32),
        ('hdir', ctypes.c_uint8),
        ('hspeed', ctypes.c_int32),
        ('servo', ctypes.c_int32)
    ]

    def __init__(self, up_down: int = None,
                For_back: int = None,
                ver_horse: int = None,
                roll_horse: int = None, 
                RR_RL: int = None,
                right_left: int = None,
                servo_ : int = None,
                switches: int = None) -> None:

        self.flags = 0

        if up_down != None:
            self.flags += 1
            self.vdir = 1 if up_down > 0 else 2
            self.vspeed = abs(up_down)


        if ver_horse != None:
            self.flags += 1
            self.vdir = 3 if ver_horse > 0 else 4
            self.vspeed = abs(ver_horse)

        if roll_horse != None:
            self.flags += 1
            self.vdir = 5 if roll_horse > 0 else 6
            self.vspeed = abs(roll_horse)


        if For_back != None:
            self.flags += 1
            self.hdir = 1 if For_back < 0 else 2
            self.hspeed = abs(For_back)

        if right_left != None:
            self.flags += 1
            self.hdir = 3 if right_left > 0 else 4
            self.hspeed = abs(right_left)


        if RR_RL != None:
            self.flags += 1
            self.hdir = 5 if RR_RL < 0 else 6
            self.hspeed = abs(RR_RL) 
        
        if  servo_ != None:
            self.flags += 1
            self.servo = abs(servo_)

        if switches != 0:
            self.flags += 1
            self.switches = switches


    def __str__(self) -> str:
        fields = []
        for field in self._fields_:
            fields.append(f"{getattr(self, field[0])}")
        string = ",".join(fields).zfill(15)
        return string
