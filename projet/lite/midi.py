from pynput import keyboard

import mido

# create a new window

# create midi output port
port = mido.open_output()

global is_space_pressed
is_space_pressed = False

KEYSYM_TO_NOTE_RANK_2 = {
    97: 60,   # a -> C4
    233: 61,  # é -> C#4
    122: 62,  # z -> D4
    34: 63,   # " -> D#4
    101: 64,  # e -> E4
    114: 65,  # r -> F4
    40: 66,   # ( -> F#4
    116: 67,  # t -> G4
    45: 68,   # - -> G#4
    121: 69,  # y -> A4
    232: 70,  # è -> A#4
    117: 71,  # u -> B4
    105: 72,  # i -> C5
    231: 73,  # ç -> C#5
    111: 74,  # o -> D5
    224: 75,  # à -> D#5
    112: 76,  # p -> E5
    65106: 77,  # ^ -> F5
    61: 78,   # = -> F#5
    36: 79,   # $ -> G5
}

KEYSYM_TO_NOTE_RANK_1 = {
    60: 47,  # < -> B2
    119: 48,  # w -> C3
    115: 49,  # s -> C#3
    120: 50,  # x -> D3
    100: 51,  # d -> D#3
    99: 52,  # c -> E3
    118: 53,  # v -> F3
    103: 54,  # g -> F#3
    98: 55,  # b -> G3
    104: 56,  # h -> G#3
    110: 57,  # n -> A3
    106: 58,  # j -> A#3
    44: 59,  # , -> B3
    59: 60,  # ; -> C4
    108: 61,  # l -> C#4
    58: 62,  # : -> D4
    109: 63,  # m -> D#4
    33: 64,  # ! -> E4
    42: 66,  # * -> F#4
}

def get_note_from_keycode(keycode):
    if keycode == 0:
        return 0

    if keycode in KEYSYM_TO_NOTE_RANK_2:
        return KEYSYM_TO_NOTE_RANK_2[keycode]

    if keycode in KEYSYM_TO_NOTE_RANK_1:
        return KEYSYM_TO_NOTE_RANK_1[keycode]

    return -1

# catch key press events
def key_press(keycode):
    # get the note to play
    note = get_note_from_keycode(keycode)
    if note == -1:
        return
    if note == 0:
        global is_space_pressed
        if is_space_pressed:
            msg = mido.Message('note_off', note=note, velocity=64)
            port.send(msg)
            is_space_pressed = False
        else:
            msg = mido.Message('note_on', note=note, velocity=64)
            port.send(msg)
            is_space_pressed = True
        return

    # create a new note on message
    msg = mido.Message('note_on', note=note, velocity=64)
    # send the message to the midi port
    port.send(msg)


# catch key release events
def key_release(keycode):
    # check if the key released is in the dictionary
    note = get_note_from_keycode(keycode)
    if note == -1 or note == 0:
        return
    # create a new note off message
    msg = mido.Message('note_off', note=note, velocity=64)
    # send the message to the midi port
    port.send(msg)

# Dictionnaire pour suivre les touches enfoncées
keys_pressed = {}

def on_press(key: keyboard.Key):
    try:
        if key.vk not in keys_pressed:
            print(f"DOWN: {key.vk}")
            keys_pressed[key.vk] = True
            key_press(key.vk)
    except AttributeError:
        if key == keyboard.Key.space and 0 not in keys_pressed:
            print(f"DOWN: {key}")
            keys_pressed[0] = True
            key_press(0)
            return
        print(f"SPE DOWN: {key}")

def on_release(key: keyboard.Key):
    try:
        if key.vk in keys_pressed:
            print(f"UP: {key.vk}")
            del keys_pressed[key.vk]
            key_release(key.vk)
    except AttributeError:
        if key == keyboard.Key.space and 0 in keys_pressed:
            print(f"UP: {key}")
            del keys_pressed[0]
            key_release(0)
            return
        print(f"SPE UP: {key}")

# Démarre l'écoute des événements clavier
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
