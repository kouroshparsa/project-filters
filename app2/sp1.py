import os
from hl7_tea import Message
msg = Message(os.getenv('msg'))
res = msg
res.set_field('GT1-1', '123')
print(res.get_field('GT1-1'))
control_id = res.get_field('MSH-10')
print(f'control id={control_id}')
