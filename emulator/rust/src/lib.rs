use std::process;

const        XX_BIT : u64 = 64;
const    CODE_START : usize = 0x8000;
const KEYBOARD_ADDR : usize = 0x6000;
const  SCREEN_START : i64 = 0x4000;
const    SCREEN_END : i64 = 0x5fff;

/*
const    DATA_START : u64 = 0;
const      DATA_END : u64 = 0x3fff;
const     DATA_SIZE : u64 = DATA_END - DATA_START + 1;
const   SCREEN_SIZE : u64 = SCREEN_END - SCREEN_START + 1;
const RESERVED_SIZE : u64 = 0x1fff;
const KEYBOARD_SIZE : u64 = 1;
const      CODE_END : usize = 0xfffff;
const     CODE_SIZE : usize = CODE_END - CODE_START + 1;
*/

pub struct Emu {
    // Registers
    pc: i64,
    ra: i64,
    rd: i64,
    rm: i64,

    // Memory
    ram: Vec<u64>,
}

impl Emu {
    pub fn new() -> Emu {
        Emu {
            // Registers
            pc: 0,
            ra: 0,
            rd: 0,
            rm: 0,

            // Memory
            ram: vec![0; 0x100000],
        }
    }
    
    pub fn load_rom(&mut self, code: &str) {
        // TODO: Sanitize file input
        let mut line_counter = 0;
        for line in code.lines() {
            let mut opcode: u64 = 0;
            for (i,c) in line.chars().enumerate() {
                let current_bit = c as u64 - '0' as u64;
                opcode |= current_bit << (63-i);
            }
            self.ram[CODE_START+line_counter] = opcode as u64;
            line_counter += 1;
        }
    }

    pub fn reset(&mut self) {
        // Clear registers
        self.pc = 0;
        self.ra = 0;
        self.rd = 0;
        self.rm = 0;

        // Clear memory
        for i in 0..self.ram.len() {
            self.store_ram(i as i64, 0);
        }
    }

    pub fn load_ram(&mut self, addr: u64) -> u64 {
        self.ram[addr as usize]
    }
    
    pub fn store_ram(&mut self, addr: i64, val: i64) {
        self.ram[addr as usize] = val as u64;

        //TODO: Only update the canvas for addresses in screen memory.
        if addr>=SCREEN_START && addr<=SCREEN_END {
            let scr_addr = addr - SCREEN_START;
            for i in (0..16).rev() {
                if val & (1<<i) != 0 {
                    //emu.set_xy(((x*16)+i, y), black):
                } else {
                    //emu.set_xy(((x*16)+i, y), white):
                }
            }
        }
    }

    pub fn key_up(&mut self) {
        self.ram[KEYBOARD_ADDR] = 0;
    }

    pub fn key_down(&mut self, code: u64) {
        self.ram[KEYBOARD_ADDR] = code;
    }

    pub fn ticks(&mut self, no_of_ticks: u32) {
        for _i in 0..no_of_ticks {
            self.tick();
        }
    }

    pub fn tick(&mut self) {

        self.rm = self.ram[self.ra as usize] as i64;
        let inst = self.ram[CODE_START+self.pc as usize];
        //println!("pc: {}, ra: {}, rd: {}, rm: {}, inst: {}", self.pc, self.ra, self.rd, self.rm, inst);

        if inst >> (XX_BIT-1) == 1 {

            // C Instructions (dest=comp;jump)
            let comp = (inst & 0x1fc0) >> 6;
            let dest = (inst & 0x0038) >> 3;
            let jump = (inst & 0x0007) >> 0;
            let comp_res: i64 = match comp {

                /*  0  */ 0x2a => 0,
                /*  1  */ 0x3f => 1,
                /* -1  */ 0x3a => -1,
                /*  D  */ 0x0c => self.rd,
                /*  A  */ 0x30 => self.ra,
                /* !D  */ 0x0d => !self.rd,
                /* !A  */ 0x31 => !self.ra,
                /* -D  */ 0x0f => -self.rd,
                /* -A  */ 0x33 => -self.ra,
                /* D+1 */ 0x1f => self.rd+1,
                /* A+1 */ 0x37 => self.ra+1,
                /* D-1 */ 0x0e => self.rd-1,
                /* A-1 */ 0x32 => self.ra-1,
                /* D+A */ 0x02 => self.rd+self.ra,
                /* D-A */ 0x23 => self.rd-self.ra,
                /* D-A */ 0x13 => self.rd-self.ra, //FIXME
                /* A-D */ 0x07 => self.ra-self.rd,
                /* D&A */ 0x00 => self.rd&self.ra,
                /* D|A */ 0x15 => self.rd|self.ra,
                /*  M  */ 0x70 => self.rm,
                /* !M  */ 0x71 => !self.rm,
                /* -M  */ 0x73 => -self.rm,
                /* M+1 */ 0x77 => self.rm+1,
                /* M-1 */ 0x72 => self.rm-1,
                /* D+M */ 0x42 => self.rd+self.rm,
                /* D-M */ 0x53 => self.rd-self.rm,
                /* M-D */ 0x47 => self.rm-self.rd,
                /* D&M */ 0x40 => self.rd&self.rm,
                /* D|M */ 0x55 => self.rd|self.rm,

                // Extended mul and div instructions:
                /* M*D */ 0x41 => self.rm*self.rd,
                /* M/D */ 0x43 => self.rm/self.rd,
                _ => {
                    println!("Invalid comp value {:x}", comp);
                    0
                }
            };

            // NOTE:
            // The order of statements below matter. DON'T change them.
            // For example: In AM=M+1, if you do A=M+1 before M=M+1,
            // M=M+1 will use M updated by A=M+1, because M depends on A.
            
            match dest {
                /*     */ 0x00 => {},
                /* M   */ 0x01 => {
                /*     */     self.store_ram(self.ra, comp_res);
                /*     */ },
                /* D   */ 0x02 => {
                /*     */     self.rd = comp_res;
                /*     */ },
                /* MD  */ 0x03 => {
                /*     */     self.store_ram(self.ra, comp_res);
                /*     */     self.rd = comp_res;
                /*     */ },
                /* A   */ 0x04 => {
                /*     */     self.ra = comp_res;
                /*     */ },
                /* AM  */ 0x05 => {
                /*     */     self.store_ram(self.ra, comp_res);
                /*     */     self.ra = comp_res;
                /*     */ },
                /* AD  */ 0x06 => {
                /*     */     self.ra = comp_res;
                /*     */     self.rd = comp_res;
                /*     */ },
                /* AMD */ 0x07 => {
                /*     */     self.store_ram(self.ra, comp_res);
                /*     */     self.ra = comp_res;
                /*     */     self.rd = comp_res;
                /*     */ },
                /*     */ _ => {}
            };

            let jump_res = match jump {
                /* INC */ 0x00 => false, // pc += 1
                /* JGT */ 0x01 => (comp_res as i64) > 0,
                /* JEQ */ 0x02 => (comp_res as i64) == 0,
                /* JGE */ 0x03 => (comp_res as i64) >= 0,
                /* JLT */ 0x04 => (comp_res as i64) < 0,
                /* JNE */ 0x05 => (comp_res as i64) != 0,
                /* JLE */ 0x06 => (comp_res as i64) <= 0,
                /* JMP */ 0x07 => true, // Unconditional
                _ => {false}
            };

            if jump_res == true {
                self.pc = self.ra-1;
            }
        } else {
            // A Instructions
            self.ra = (inst & 0x7fffffffffffffff) as i64
        }

        self.pc += 1;
    }
    
    pub fn draw(&mut self, frame: &mut [u8]) {
        for (i, pixel) in frame.chunks_exact_mut(4).enumerate() {
            let is_pixel_set =
                (self.load_ram(0x4000 + (i/16) as u64) >> (i%16)) & 1;
            let rgba = if is_pixel_set != 0 {
                [0x00, 0x00, 0x00, 0xff]
            } else {
                [0xff, 0xff, 0xff, 0xff]
            };
            pixel.copy_from_slice(&rgba);
        }
    }
}
