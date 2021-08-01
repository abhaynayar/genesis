#include <SDL2/SDL.h>
#include <vector>
#include <bitset>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>

#define SCREEN_WIDTH 512
#define SCREEN_HEIGHT 256

#define ROM_OFFSET 0x8000
#define CODE_START 0x8000
#define RAM_SIZE   0x100000

void err(std::string e) {
    std::cout << e << std::endl;
    exit(0);
}

class Emu {
public:

    int64_t pc, ra, rd, rm;
    std::vector<uint64_t> ram;
    SDL_Renderer* m_renderer;

    Emu(SDL_Renderer* renderer): m_renderer(renderer), ram(RAM_SIZE,0) {}

    void set_pixel(int x, int y, int color) {
        if (x>SCREEN_WIDTH || y>SCREEN_HEIGHT || x<0 || y<0) return;
        SDL_SetRenderDrawColor(m_renderer, color, color, color, SDL_ALPHA_OPAQUE);
        SDL_RenderDrawPoint(m_renderer, x, y);
        SDL_RenderPresent(m_renderer);
    }

    void store_ram(uint64_t address, uint64_t value) {
        if (address > 0xFFFFF) {
            err("We are in disk.");
        }

        ram[address] = value;
        uint64_t screen_address = address - 0x4000;
        if (screen_address < 0) return;

        uint64_t x = int(screen_address % 32);
        uint64_t y = int(screen_address / 32);

        for (int i=15; i>=0; --i) {
            int set = value & (1<<i);
            if (set != 0) {
                set_pixel((x*16)+i, y, 0x00);
            } else {
                set_pixel((x*16)+i, y, 0xFF);
            }
        }
    }

    void load_rom(std::vector<std::string> &file_contents) {
        for (int i=0; i<file_contents.size(); ++i) {
            //std::cout << file_contents[i] << std::endl;
            ram[ROM_OFFSET+i] = std::bitset<64>(file_contents[i]).to_ullong();
        }
        std::cout << "ROM loaded." << std::endl;
    }

    uint64_t comp_exe(uint64_t comp) {
        switch (comp) {
            /*  0  */ case 0x2a: return 0;
            /*  1  */ case 0x3f: return 1;
            /* -1  */ case 0x3a: return 0xffffffffffffffff;
            /*  D  */ case 0x0c: return rd;
            /*  A  */ case 0x30: return ra;
            /* !D  */ case 0x0d: return ~rd;
            /* !A  */ case 0x31: return ~ra;
            /* -D  */ case 0x0f: return -rd;
            /* -A  */ case 0x33: return -ra;
            /* D+1 */ case 0x1f: return rd+1;
            /* A+1 */ case 0x37: return ra+1;
            /* D-1 */ case 0x0e: return rd-1;
            /* A-1 */ case 0x32: return ra-1;
            /* D+A */ case 0x02: return rd+ra;
            /* D-A */ case 0x23: return rd-ra;
            /* D-A */ case 0x13: return rd-ra; //FIXME
            /* A-D */ case 0x07: return ra-rd;
            /* D&A */ case 0x00: return rd&ra;
            /* D|A */ case 0x15: return rd|ra;
            /*  M  */ case 0x70: return rm;
            /* !M  */ case 0x71: return ~rm;
            /* -M  */ case 0x73: return -rm;
            /* M+1 */ case 0x77: return rm+1;
            /* M-1 */ case 0x72: return rm-1;
            /* D+M */ case 0x42: return rd+rm;
            /* D-M */ case 0x53: return rd-rm;
            /* M-D */ case 0x47: return rm-rd;
            /* D&M */ case 0x40: return rd&rm;
            /* D|M */ case 0x55: return rd|rm;
            /* M*D */ case 0x41: return rm*rd;
            /* M/D */ case 0x43: return rm/rd;
            default: err("Invalid comp value " + std::to_string(comp)); return -1;
        };
    }

    void dest_exe(uint64_t dest, uint64_t comp_res) {
        switch (dest) {
            case 0x00:
                break;
            case 0x01:
                store_ram(ra, comp_res);
                break;
            case 0x02:
                rd = comp_res;
                break;
            case 0x03:
                store_ram(ra, comp_res);
                rd = comp_res;
                break;
            case 0x04:
                ra = comp_res;
                break;
            case 0x05:
                store_ram(ra, comp_res);
                ra = comp_res;
                break;
            case 0x06:
                ra = comp_res;
                rd = comp_res;
                break;
            case 0x07:
                store_ram(ra, comp_res);
                ra = comp_res;
                rd = comp_res;
                break;
            default:
                err("Invalid dest value");
        }
    }

    bool jump_exe(uint64_t jump, uint64_t ucomp_res) {
        int64_t comp_res = (int64_t) ucomp_res;

        switch (jump) {
            /* INC */ case 0x00: return false; // pc += 1
            /* JGT */ case 0x01: return comp_res > 0;
            /* JEQ */ case 0x02: return comp_res == 0;
            /* JGE */ case 0x03: return comp_res >= 0;
            /* JLT */ case 0x04: return comp_res < 0;
            /* JNE */ case 0x05: return comp_res != 0;
            /* JLE */ case 0x06: return comp_res <= 0;
            /* JMP */ case 0x07: return true; // Unconditional
            default: err("Invalid jump value"); return false;
        }
    }

    uint64_t load_ram(uint64_t address) {
        if ((address < 0) || (address > RAM_SIZE)) {
            std::cout << "Invalid RAM address: " << address << std::endl;
            exit(-1);
        }
        return ram[address];
    }

    void tick() {
        rm = load_ram(ra);
        uint64_t inst = load_ram(ROM_OFFSET+pc);
        //printf("pc: %llu, ra: %llu, rd: %llu, rm: %llu, inst: %llu\n", pc, ra, rd, rm, inst);

        if ((inst >> 63) == 1) {
            uint64_t comp = (inst & 0x1fc0) >> 6;
            uint64_t dest = (inst & 0x0038) >> 3;
            uint64_t jump = (inst & 0x0007) >> 0;

            uint64_t comp_res = comp_exe(comp);
            dest_exe(dest, comp_res);
            bool jump_res = jump_exe(jump, comp_res);

            if (jump_res != false) {
                pc = ra-1;
            }

        } else {
            ra = inst & 0x7fffffffffffffff;
        }

        pc++;
    }
};

int main(int argc, char** argv){

    if(argc != 2) {
        puts("usage: emu [HACK_FILE]");
        return 1;
    }

    // File
    std::string arg1(argv[1]);
    std::ifstream infile; infile.open(arg1, std::ios::in);
    std::vector<std::string> file_contents; std::string temp;
    while(getline(infile, temp)) file_contents.push_back(temp);
    infile.close();

    // Gfx
    SDL_Init(SDL_INIT_EVERYTHING);

    SDL_Window* window = SDL_CreateWindow (
        "SDL2", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
        SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN
    );
    
    SDL_Renderer* renderer = SDL_CreateRenderer (
        window, -1, SDL_RENDERER_ACCELERATED
    );

    SDL_Event event;
    bool running = true;

    // Emulator
    Emu emu(renderer);
    emu.load_rom(file_contents);

    SDL_SetRenderDrawColor(renderer, 0x00, 0x00, 0x00, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);
    SDL_RenderPresent(renderer);

    SDL_SetRenderDrawColor(renderer, 0xFF, 0xFF, 0xFF, SDL_ALPHA_OPAQUE);
    SDL_RenderDrawPoint(renderer, 10, 10);
    SDL_RenderPresent(renderer);
    puts("Starting emulator.");

    int i=0;

    // Loop
    while (running) {
        emu.tick();
        while (SDL_PollEvent(&event)) {
            if ((SDL_QUIT == event.type) || (SDL_KEYDOWN == event.type &&
                        SDL_SCANCODE_ESCAPE == event.key.keysym.scancode)) {
                running = false;
                break;
            }
        }
        i++;
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}