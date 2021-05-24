pub struct Emu {
    // Registers
    pc: u16, ra: u16,
    rd: u16, rm: u16,

    // Memory
    rom: [u16; 0x8000],
    ram: [u16; 0x8000],

    // Debug
    cycle: u64,
    pause: bool,
}


impl Emu {
    pub fn new() -> Emu {
        Emu {
            // Registers
            pc: 0, ra: 0,
            rd: 0, rm: 0,

            // Memory
            rom: [0; 0x8000],
            ram: [0; 0x8000],

            // Debug
            cycle: 0,
            pause: false,
        }
    }

    pub fn ticks(&mut self, no_of_ticks: u32) {
        for _i in 0..no_of_ticks {
            self.tick();
        }

        self.key_up();
    }

    pub fn reset(&mut self) {
        // Clear registers
        self.pc = 0;
        self.ra = 0;
        self.rd = 0;
        self.rm = 0;

        // Clear memory
        for x in 0..self.ram.len() { self.store_ram(x as u16,0); }

        // Clear debug tools
        self.cycle = 0;
        self.pause = false;
    }
    
    pub fn store_ram(&mut self, addr: u16, val: u16) {
        self.ram[addr as usize] = val;

        // Only update the canvas for addresses in screen memory
        if addr>=0x4000 && addr<0x6000 {
            //put_xy(addr,val);
        }
    }
    
    // TODO: Sanitize ROM input
    pub fn load_rom(&mut self, code: &str) {
        // TODO: Check if code is empty
        let mut line_counter = 0;
        for line in code.lines() {
            let mut opcode: u16 = 0;
            for (i,c) in line.chars().enumerate() {
                let current_bit = c as u16 - '0' as u16;
                opcode |= current_bit << (15-i);
            }
            self.rom[line_counter] = opcode;
            line_counter += 1;
        }
    }

    pub fn load_ram(&mut self, addr: u16) -> u16 {
        self.ram[addr as usize]
    }
 
    pub fn key_down(&mut self, code: u16) {
        self.ram[0x6000] = code;
    }

    pub fn key_up(&mut self) {
        self.ram[0x6000] = 0;
    }

    pub fn tick(&mut self) {

        self.rm = self.ram[self.ra as usize];
        let inst = self.rom[self.pc as usize];
        //println!("pc: {}, ra: {}, rd: {}, rm: {}, inst: {}\n",
        //self.pc, self.ra, self.rd, self.rm, inst);

        if inst >> 15 == 1 {

            // C Instructions (dest=comp;jump)
            let comp = (inst & 0x1fc0) >> 6;
            let dest = (inst & 0x0038) >> 3;
            let jump = (inst & 0x0007) >> 0;
            let comp_res: u16 = match comp {

                /*  0  */ 0x2a => 0,
                /*  1  */ 0x3f => 1,
                /* -1  */ 0x3a => 0xffff, //-(1 as i16) as u16,
                /*  D  */ 0x0c => self.rd,
                /*  A  */ 0x30 => self.ra,
                /* !D  */ 0x0d => !self.rd,
                /* !A  */ 0x31 => !self.ra,
                /* -D  */ 0x0f => -(self.rd as i16) as u16,
                /* -A  */ 0x33 => -(self.ra as i16) as u16,
                /* D+1 */ 0x1f => (self.rd as i16).wrapping_add(1) as u16,
                /* A+1 */ 0x37 => (self.ra as i16).wrapping_add(1) as u16,
                /* D-1 */ 0x0e => (self.rd as i16).wrapping_sub(1) as u16,
                /* A-1 */ 0x32 => (self.ra as i16).wrapping_sub(1) as u16,
                /* D+A */ 0x02 => ((self.rd as i16).wrapping_add(self.ra as i16)) as u16,
                /* D-A */ 0x23 => ((self.rd as i16).wrapping_sub(self.ra as i16)) as u16,
                /* D-A */ 0x13 => ((self.rd as i16).wrapping_sub(self.ra as i16)) as u16, //FIXME
                /* A-D */ 0x07 => ((self.ra as i16).wrapping_sub(self.rd as i16)) as u16,
                /* D&A */ 0x00 => self.rd & self.ra,
                /* D|A */ 0x15 => self.rd | self.ra,
                /*  M  */ 0x70 => self.rm,
                /* !M  */ 0x71 => !self.rm,
                /* -M  */ 0x73 => -(self.rm as i16) as u16,
                /* M+1 */ 0x77 => (self.rm as i16).wrapping_add(1) as u16,
                /* M-1 */ 0x72 => (self.rm as i16).wrapping_sub(1) as u16,
                /* D+M */ 0x42 => ((self.rd as i16).wrapping_add(self.rm as i16)) as u16,
                /* D-M */ 0x53 => ((self.rd as i16).wrapping_sub(self.rm as i16)) as u16,
                /* M-D */ 0x47 => ((self.rm as i16).wrapping_sub(self.rd as i16)) as u16,
                /* D&M */ 0x40 => self.rd & self.rm,
                /* D|M */ 0x55 => self.rd | self.rm,

                //heinz
                /* M*D */ 0x41 => (self.rm * self.rd) as u16,
                /* M/D */ 0x43 => (self.rm / self.rd) as u16,
                _ => {1337}
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
                /* JGT */ 0x01 => (comp_res as i16) > 0,
                /* JEQ */ 0x02 => (comp_res as i16) == 0,
                /* JGE */ 0x03 => (comp_res as i16) >= 0,
                /* JLT */ 0x04 => (comp_res as i16) < 0,
                /* JNE */ 0x05 => (comp_res as i16) != 0,
                /* JLE */ 0x06 => (comp_res as i16) <= 0,
                /* JMP */ 0x07 => true, // Unconditional
                _ => {false}
            };

            if jump_res == true {
                self.pc = self.ra-1;
            }
        } else {
            // A Instructions
            self.ra = inst & 0x7fff;
        }

        self.pc += 1;
        self.cycle += 1;
    }
    
    pub fn draw(&mut self, frame: &mut [u8]) {
        for (i, pixel) in frame.chunks_exact_mut(4).enumerate() {
            let is_pixel_set =
                (self.load_ram(0x4000 + (i/16) as u16) >> (i%16)) & 1;
            let rgba = if is_pixel_set != 0 {
                [0x00, 0x00, 0x00, 0xff]
            } else {
                [0xff, 0xff, 0xff, 0xff]
            };
            pixel.copy_from_slice(&rgba);
        }
    }
}
