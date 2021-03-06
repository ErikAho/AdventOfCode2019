import time

print('\nRunning Day 2 Script\n')

start_time = time.time()


def get_initial_state():  # could do with deep copy instead of fetching each time
    with open('02/input.txt', 'r') as input_file:
        return list(map(int, input_file.read().split(',')))


def perform_action(array, index):
    (Opcode, pos1, pos2, pos3) = array[index:index + 4]
    if Opcode == 1:
        array[pos3] = array[pos1] + array[pos2]
        return False  # should not halt
    elif Opcode == 2:
        array[pos3] = array[pos1] * array[pos2]
        return False  # should not halt
    elif Opcode == 99:
        return True  # should halt
    else:
        return True  # encountered error


def run_intcode(intcode_arr):
    i = 0
    while i < len(intcode_arr):
        if perform_action(intcode_arr, i):  # true in case of Opcode 99
            break
        else:
            i += 4
    return intcode_arr


if __name__ == '__main__':
    intcode = get_initial_state()
    # initialize with constants from question
    intcode[1] = 12
    intcode[2] = 2

    print('\nPart 1: \nOutput for first task:', (run_intcode(intcode))[0])

    target_output = 19690720

    print('\nPart 2: \nSearching for Noun + Verb combinations... \n')
    for noun in range(100):
        for verb in range(100):
            memory = get_initial_state()
            memory[1] = noun
            memory[2] = verb
            if run_intcode(memory)[0] == target_output:
                print('Success! Noun * 100 + Verb ==', (noun * 100 + verb))

    end_time = time.time()
    print('\nTime to complete: %.4fs' % (end_time - start_time))
