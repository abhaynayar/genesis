import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import struct
import ctypes

################################################
# Some pygame config.

(white, black)  = ((255,255,255), (0,0,0))
(width, height) = (512, 256)
screen = pygame.display.set_mode((width, height))
screen.fill(white)
pygame.display.update()

################################################
# Thoughts on the new RAM and what will be where:
"""
Right now, every program that we store in the RAM will need to have its own
operating system since we lose all information after we assemble. One way to
solve this problem is to assemble it in the emulator.

But, this is not a good thing. The CPU emulator should only process bits.

Yes, the entire operating system has to be written and compiled beforehand of
course. What was I thinking lol. So you just build the operating system and put
it in the large-ass RAM. That's how operating systems work??? Later on we can
start doing more stuff once we have access to external storage and file systems.
"""

################################################
# Now that we have a von-Neumann architecture, we are still keeping some area
# reserved in the beginning for some read-only code that is kind of like a
# bootstrap code. The below offset is where our big-ass RAM starts.
RAM_OFFSET = 0x8000


################################################
# The emulator class.
class Emu:

    ram = []

    pc = 0
    ra = 0
    rd = 0
    rm = 0

    def __init__(self):
        for i in range(0x8000*4):
            self.ram.append(0)

        infile = open(sys.argv[1]).readlines()
        for i,line in enumerate(infile):
            self.ram[i] = int(line,2)

    def dump_regs(self, inst):
        print('pc:', self.pc, end=', ')
        print('ra:', self.ra, end=', ')
        print('rd:', self.rd, end=', ')
        print('rm:', self.rm, end=', ')
        print('inst:', inst)
    
    def store_ram(self, address, value):
        self.ram[RAM_OFFSET + address] = value
    
        # if address>=0x4000 and address<0x6000:
        screen_address = address - 0x4000
        if screen_address < 0: return
        
        x = int(screen_address % 32)
        y = int(screen_address / 32)
        for i in range(15,-1,-1):
            set1 = value & (1<<i)
            if (set1 != 0): screen.set_at(((x*16)+i, y), black)
            else: screen.set_at(((x*16)+i, y), white)
        pygame.display.flip()
    
    def get_comp_res(self, comp):
        if comp == 0x2a: return 0
        if comp == 0x3f: return 1
        if comp == 0x3a: return -1
        if comp == 0x0c: return self.rd
        if comp == 0x30: return self.ra
        if comp == 0x0d: return ~self.rd
        if comp == 0x31: return ~self.ra
        if comp == 0x0f: return -self.rd
        if comp == 0x33: return -self.ra
        if comp == 0x1f: return self.rd+1
        if comp == 0x37: return self.ra+1
        if comp == 0x0e: return self.rd-1
        if comp == 0x32: return self.ra-1
        if comp == 0x02: return self.rd+self.ra
        if comp == 0x23: return self.rd-self.ra
        if comp == 0x13: return self.rd-self.ra #FIXME
        if comp == 0x07: return self.ra-self.rd
        if comp == 0x00: return self.rd&self.ra
        if comp == 0x15: return self.rd|self.ra
        if comp == 0x70: return self.rm
        if comp == 0x71: return ~self.rm
        if comp == 0x73: return -self.rm
        if comp == 0x77: return self.rm+1
        if comp == 0x72: return self.rm-1
        if comp == 0x42: return self.rd+self.rm
        if comp == 0x53: return self.rd-self.rm
        if comp == 0x47: return self.rm-self.rd
        if comp == 0x40: return self.rd&self.rm
        if comp == 0x55: return self.rd|self.rm

        # These are extended multiplication and division instructions:
        if comp == 0x41: return self.rm*self.rd
        if comp == 0x43: return int(self.rm/self.rd)
    
    def dest_res(self, dest, comp_res):
        if dest == 1: self.store_ram(self.ra, comp_res)
        if dest == 2: self.rd = comp_res
        if dest == 3:
            # if comp_res >= 0x4000: print(hex(comp_res))
            self.store_ram(self.ra, comp_res)
            self.rd = comp_res
        if dest == 4: self.ra = comp_res
        if dest == 5:
            self.store_ram(self.ra, comp_res)
            self.ra = comp_res
        if dest == 6: self.ra = self.rd = comp_res
        if dest == 7:
            self.store_ram(self.ra, comp_res)
            self.ra = self.rd = comp_res
    
    def jump_res(self, jump, comp_res):
        # Need to be signed for comparisons
        comp_res = ctypes.c_short(comp_res).value
        if jump == 0: return False
        if jump == 1: return comp_res > 0
        if jump == 2: return comp_res == 0
        if jump == 3: return comp_res >= 0
        if jump == 4: return comp_res < 0
        if jump == 5: return comp_res != 0
        if jump == 6: return comp_res <= 0
        if jump == 7: return True
    
    def tick(self):
        self.rm = self.ram[RAM_OFFSET+self.ra]
        inst = self.ram[self.pc]
        # self.dump_regs(inst)

        if (inst>>15) == 1: # C Instruction:
            # dest(5-3)=comp(12-6);jump(2-0)
            comp = (inst & 0x1fc0) >> 6
            dest = (inst & 0x0038) >> 3
            jump = (inst & 0x0007) >> 0
    
            # Results
            comp_res = ctypes.c_ushort(self.get_comp_res(comp)).value
            comp_res = comp_res & 0xffff
            self.dest_res(dest, comp_res)
            if self.jump_res(jump, comp_res) == True:
                self.pc = self.ra-1
        
        # A Intruction:
        else: self.ra = inst & 0x7fff
        self.pc += 1

emu = Emu()

################################################
# Main driver program:
running = True
while running:
    emu.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
