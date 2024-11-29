import os
from hl7_tea import Message
msg = Message(os.getenv('msg'))

print('hi')
print(msg)
res = msg
