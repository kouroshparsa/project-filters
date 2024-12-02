import os
from hl7_tea import Message
msg = Message(os.getenv('msg'))
res = msg
res.set_field('GT1-1', '123')
