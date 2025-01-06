import os
from hl7_tea import Message

SIU_LUT = ["S12","S13","S14","S15","S23","S26"]

try:
    import lookup
    SIU_LUT = lookup.get_lut('SIU_TriggerEvents')
except Exception as ex:
    print(f'SIU_TriggerEvents is not set for the app. {ex}')

def filter_message(msg: Message):
    if msg.message_type == 'SIU':
        if msg.trigger_event not in SIU_LUT:
            print(msg.trigger_event, ' is not in',  SIU_LUT)
        return msg.trigger_event in SIU_LUT
    return False


msg = Message(os.getenv('msg'))
msg.promote({'message_type': 'MSH-9.1',
             'trigger_event': 'MSH-9.2'})
print('message_type=', msg.message_type)

if not filter_message(msg):
    res = None
    print('filtered out')
else:
    res = msg.direct_map('MSH', 'SCH-6', 'SCH-9', 'SCH-10', 'SCH-11', 'SCH-25',
                         'PID-1', 'PID-5', 'PID-7', 'PID-8', 'PID-11', 'PID-13', 'PID-18', 'PID-19',
                         'AIS-1', 'AIS-3',
                         'ZAL-1')

    for zfh in msg.segments.get('ZFH', []):
        if zfh[1] == 'Savience':
            res.segments['ZFH'].append(['', zfh[2], zfh[3], '', zfh[5]])
        elif zfh[1] == 'CVC':
            res.segments['ZFH'].append([zfh[1], zfh[2], zfh[3], '', '' ,'' ,'', '', '', '', '', '', zfh[13], zfh[14], '', '', zfh[17]])

