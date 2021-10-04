import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import ctypes

################################################
# Initializing file system:
fs = open('disk.img', 'r+b') # Read and write (binary file)

################################################
# Error stub:
def err(x):
    print(x)
    exit()

################################################
# Some consts.
XX_BIT = 64

DATA_START = 0
DATA_END   = 0x3fff
DATA_SIZE  = DATA_END - DATA_START + 1

SCREEN_START = 0x4000
SCREEN_END   = 0x5fff
SCREEN_SIZE  = SCREEN_END - SCREEN_START + 1

KEYBOARD_ADDR = 0x6000
KEYBOARD_SIZE = 1
RESERVED_SIZE = 0x1fff

CODE_START = 0x8000
CODE_END   = 0xfffff
CODE_SIZE  = CODE_END - CODE_START + 1

################################################
# Some pygame config.

(white, black)  = ((255,255,255), (0,0,0))
resolution = (width, height) = (512, 256)
flags = pygame.DOUBLEBUF

screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
screen.set_alpha(None)
screen.fill(white)

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.display.update()

key_translation = {
    13: 128, #newline
    8:  129, #backspace
    1073741904: 130, #left
    1073741906: 131, #up
    1073741903: 132, #right
    1073741905: 133, #down
    1073741898: 134, #home
    1073741901: 135, #end
    1073741899: 136, #pgup
    1073741902: 137, #pgdn
    1073741897: 138, #insert
    127: 139, #delete
    27:  140, #escape
    1073741882: 141, #f1
    1073741883: 142, #f2
    1073741884: 143, #f3
    1073741885: 144, #f4
    1073741886: 145, #f5
    1073741887: 146, #f6
    1073741888: 147, #f7
    1073741889: 148, #f8
    1073741890: 149, #f9
    1073741891: 150, #f10
    1073741892: 151, #f11
    1073741893: 152, #f12
}

################################################
# The emulator class.
class Emu:

    ram = [0] * (DATA_SIZE + SCREEN_SIZE + \
            KEYBOARD_SIZE +  RESERVED_SIZE + CODE_SIZE) 

    pc = 0
    ra = 0
    rd = 0
    rm = 0

    def __init__(self):
        infile = open(sys.argv[1]).readlines()
        size = 0
        for i,line in enumerate(infile):
            self.ram[CODE_START+i] = int(line,2)
            size += 1
        print(str(int((size/CODE_SIZE)*100)) + '% CODE MEMORY USED')

    def dump_regs(self, inst):
        print("pc:", self.pc, end=", ")
        print("ra:", self.ra, end=", ")
        print("rd:", self.rd, end=", ")
        print("rm:", self.rm, end=", ")
        print("inst:", inst)

    def load_ram(self, address):
        if address > 0xfffff: # We *MAY* be in disk
            fs.seek(address-0x100000)
            return ord(fs.read(1))
        else:
            return self.ram[address]

    def store_ram(self, address, value):
        if address > 0xfffff: # We are in disk
            fs.seek(address-0x100000)
            fs.write(value)
            return

        self.ram[address] = value
        if address >= SCREEN_START and address <= SCREEN_END:
            self.update_screen(address-SCREEN_START, value)
        
    def update_screen(self, address, value):
        x = int(address % 32)
        y = int(address / 32)

        # TODO: We are only looking at 16 bits instead of 64 bits
        for i in range(15,-1,-1):
            pixel = value & (1<<i)
            if (pixel != 0): screen.set_at(((x*16)+i, y), black)
            else: screen.set_at(((x*16)+i, y), white)
        pygame.display.update(pygame.Rect(x*16, y, 16, 1))

    def clear_keyboard(self):
        self.store_ram(KEYBOARD_ADDR, 0)

    def update_keyboard(self, keycode):
        global key_translation
        host = key_translation.get(keycode, keycode)
        self.store_ram(KEYBOARD_ADDR, host)
    
    def get_comp_res(self, comp):
        if comp == 0x2a: return 0
        elif comp == 0x3f: return 1
        elif comp == 0x3a: return -1
        elif comp == 0x0c: return self.rd
        elif comp == 0x30: return self.ra
        elif comp == 0x0d: return ~self.rd
        elif comp == 0x31: return ~self.ra
        elif comp == 0x0f: return -self.rd
        elif comp == 0x33: return -self.ra
        elif comp == 0x1f: return self.rd+1
        elif comp == 0x37: return self.ra+1
        elif comp == 0x0e: return self.rd-1
        elif comp == 0x32: return self.ra-1
        elif comp == 0x02: return self.rd+self.ra
        elif comp == 0x23: return self.rd-self.ra
        elif comp == 0x13: return self.rd-self.ra #TODO: HW-based emulator
        elif comp == 0x07: return self.ra-self.rd
        elif comp == 0x00: return self.rd&self.ra
        elif comp == 0x15: return self.rd|self.ra
        elif comp == 0x70: return self.rm
        elif comp == 0x71: return ~self.rm
        elif comp == 0x73: return -self.rm
        elif comp == 0x77: return self.rm+1
        elif comp == 0x72: return self.rm-1
        elif comp == 0x42: return self.rd+self.rm
        elif comp == 0x53: return self.rd-self.rm
        elif comp == 0x47: return self.rm-self.rd
        elif comp == 0x40: return self.rd&self.rm
        elif comp == 0x55: return self.rd|self.rm

        #  Extended multiplication and division instructions:
        elif comp == 0x41: return self.rm*self.rd
        elif comp == 0x43: return int(self.rm/self.rd)
        else: err("Invalid comp value: " + hex(comp))
    
    def dest_res(self, dest, comp_res):
        if dest == 1: self.store_ram(self.ra, comp_res)
        elif dest == 2: self.rd = comp_res
        elif dest == 3:
            # if comp_res >= 0x4000: print(hex(comp_res))
            self.store_ram(self.ra, comp_res)
            self.rd = comp_res
        elif dest == 4: self.ra = comp_res
        elif dest == 5:
            self.store_ram(self.ra, comp_res)
            self.ra = comp_res
        elif dest == 6: self.ra = self.rd = comp_res
        elif dest == 7:
            self.store_ram(self.ra, comp_res)
            self.ra = self.rd = comp_res
    
    def jump_res(self, jump, comp_res):
        # Signed for comparisons:
        comp_res = ctypes.c_int64(comp_res).value #milch
        if jump == 0: return False
        if jump == 1: return comp_res > 0
        if jump == 2: return comp_res == 0
        if jump == 3: return comp_res >= 0
        if jump == 4: return comp_res < 0
        if jump == 5: return comp_res != 0
        if jump == 6: return comp_res <= 0
        if jump == 7: return True
    
    def tick(self):
        self.rm = self.load_ram(self.ra)
        inst = self.load_ram(CODE_START+self.pc)
        # self.dump_regs(inst)

        if (inst>>XX_BIT-1) == 1: # C Instruction: #milch
            # dest(5-3)=comp(12-6);jump(2-0)
            comp = (inst & 0x1fc0) >> 6
            dest = (inst & 0x0038) >> 3
            jump = (inst & 0x0007) >> 0
    
            # Results
            comp_res = ctypes.c_uint64(self.get_comp_res(comp)).value #milch
            comp_res = comp_res & 2**(XX_BIT)-1 #milch
            self.dest_res(dest, comp_res)
            if self.jump_res(jump, comp_res) == True:
                self.pc = self.ra-1
        
        # A Intruction:
        else: self.ra = inst & 2**(XX_BIT-1)-1 #milch
        self.pc += 1

emu = Emu()

# TODO: Double buffering.
# Allow only certain events:
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
ticks_per_tick = 1000 # TODO: what's the optimal value?

################################################
# Main driver program:
while 1:
    for i in range(ticks_per_tick): emu.tick()
    for event in pygame.event.get():
        if event.type==pygame.QUIT: exit(1)
        if event.type==pygame.KEYUP: emu.clear_keyboard()
        if event.type==pygame.KEYDOWN: emu.update_keyboard(event.key)
