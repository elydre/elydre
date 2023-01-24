gcc -m32 -c prog.c -o prog.o
ld -m elf_i386 -e start -o prog.pe prog.o
objcopy -O binary prog.pe prog.bin
