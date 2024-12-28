import os
from hl7_tea import Message

ADT_LUT = ["A01","A02","A03","A04","A05","A06","A07","A08","A11","A12","A13","A17","A31","A38","A40","A41","A44"]

try:
    import lookup
    ADT_LUT = lookup.get_lut('ADT_TriggerEvents')
except Exception as ex:
    print(f'ADT_TriggerEvents is not set for the app. {ex}')

def filter_message(msg: Message):
    if msg.message_type == 'ADT':
        if msg.trigger_event not in ADT_LUT:
            print(msg.trigger_event, ' is not in',  ADT_LUT)
        return msg.trigger_event in ADT_LUT
    return False


msg = Message(os.getenv('msg'))
msg.promote({'message_type': 'MSH-9.1',
             'trigger_event': 'MSH-9.2'})
print('message_type=', msg.message_type)

if not filter_message(msg):
    res = None
    print('filtered out')
else:
    res = msg.direct_map('MSH', 'EVN-1', 'EVN-2', 'EVN-4',
                         'PID-1', 'PID-2', 'PID-5', 'PID-7', 'PID-8', 'PID-11', 'PID-13', 'PID-18', 'PID-19',
                         'PV1-1', 'PV1-2', 'PV1-3', 'PV1-4', 'PV1-6', 'PV1-8', 'PV1-44',
                         'PV2-3',
                         'GT1-1', 'GT1-3',
                         'IN1-1', 'IN1-2', 'IN1-8', 'IN1-16', 'IN1-18',
                         'MRG-1', 'MRG-2', 'MRG-3')

    pid3_to_map = []
    pid4_to_map = []
    for pid3 in msg.get_repeated_fields('PID-3'):
        if pid3.get_sub(5) == 'MR':
            pid3_to_map.append(pid3)
    
        elif pid3.get_sub(5) == 'PI':
            pid4_to_map.append(pid3)

    res.set_repeated_fields(pid3_to_map)
    res.set_repeated_fields(pid4_to_map)
