import mido

with mido.open_input() as inport, mido.open_output() as outport:
    for msg in inport:
        if msg.type == 'note_on' and msg.note == 12:
            cc_value = msg.velocity
            cc_msg = mido.Message('control_change', control=11, value=cc_value)
            outport.send(cc_msg)
            print(cc_msg)
