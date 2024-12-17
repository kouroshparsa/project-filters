import os
from hl7_tea import Message

ADT_LUT = ["A01","A02","A03","A04","A05","A06","A07","A08","A11","A12","A13","A17","A31","A38","A40","A41","A44"]

try:
    import lookup
    ADT_LUT = lookup.get_lut('ADT_TriggerEvents')
    print(ADT_LUT)
except Exception as ex:
    print(f'ADT_TriggerEvents is not set for the app. {ex}')

def filter_message(msg: Message):
    if msg.message_type == 'ADT':
        return msg.trigger_event in ADT_LUT
    return False


msg = Message(os.getenv('msg'))
#res = msg
#res.set_field('GT1-1', '123')
#print(res.get_field('GT1-1').value)
msg.promote({'message_type': 'MSH-9.1',
             'trigger_event': 'MSH-9.2'})
print(msg.message_type)

if not filter_message(msg):
    res = None
    print('filtered out')
else:
    res = msg.direct_map('MSH', 'PID', 'PV1-1', 'PV1-2', 'PV1-3', 'PV1-6.1')
    control_id = res.get_field('MSH-10').value
    print(f'control id={control_id}')
