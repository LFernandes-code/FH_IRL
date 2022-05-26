#from gym_game.envs import *





key_up = -1
key_down = -1

def action(action):
    global key_down
    global key_up
    if key_down == -1:
        key_down = action
        print('generate event')
    elif action != key_down:
        key_up = key_down
        key_down = action

    print(key_down, key_up)

action(1)
action(1)
action(1)
action(0)