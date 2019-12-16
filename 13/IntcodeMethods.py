#Adjusted input system a little but otherwise same as Day 11

from collections import defaultdict

class opcode_comp:
    def __init__(self, array):
        self.memory = defaultdict(lambda: 0, enumerate(array))
        self.inputs = []
        self.output = None
        self.phase = 0
        self.finished = False
        self.isPhase = False
        self.base = 0
        self.index = 0

    def set_phase(self, val: int):
        self.isPhase = True
        self.phase = val

    def add_input(self, *inputs: int):
        for i in inputs:
            self.inputs.append(i)

    def set_input(self, input: int): #Used for paddle to remain same input until manually changed
        self.inputs = input
    
    def read_input(self) -> int:
        if self.isPhase == True:
            self.isPhase = False
            return self.phase
        else:
            if isinstance(self.inputs, int):
                return self.inputs
            else:
                return (self.inputs.pop(0))
        
    def has_finished(self):
        return self.finished
    
    def set_output(self, val:int):
        self.output = val
    
    def get_output(self):
        return self.output
    
    def change_base(self, val: int):
        self.base += val

    def interpret_params(self,modes:list):
        params = []
        for i in range(len(modes)):
            v = int(self.memory[self.index + i + 1])
            if modes[i] == '0':
                params.append(int(self.memory[v]))
            elif modes[i] == '1':
                params.append(v)
            elif modes[i] == '2':
                params.append(int(self.memory[v + self.base]))
        return params
    
    def literal_params(self, modes:list):
        params = []
        for i in range(len(modes)):
            v = int(self.memory[self.index + i + 1])
            if modes[i] == '0':
                params.append(v)
            elif modes[i] == '1':
                params.append(v)
            elif modes[i] == '2' or 2:
                params.append(v + self.base)
        return params
    
    def run(self):
        while self.finished == False:
            opcode = '0000' + str(self.memory[self.index])
            fn = opcode[-2:]
            modes = list(opcode[-3:-6:-1])
            nums = [self.memory[i] for i in range(self.index, self.index +4)]
            # print('Fn: {}, Modes: {}, Index: {}, Numbers: {}'.format(fn, modes, self.index,nums))
            if fn == '01':
                params = self.interpret_params(modes)
                write_address = self.literal_params(modes)
                self.memory[write_address[2]] = params[0] + params[1]
                self.index += 4
            elif fn == '02':
                params = self.interpret_params(modes)
                write_address = self.literal_params(modes)[2]
                self.memory[write_address] = (params[0] * params[1])
                self.index += 4
            elif fn == '03':
                write_address = self.literal_params(modes)[0]
                self.memory[write_address] = self.read_input()
                self.index += 2
            elif fn == '04':
                params = self.interpret_params(modes)
                self.set_output(params[0])
                # print('Output: ',self.output)
                self.index += 2
                break
            elif fn == '05':
                params = self.interpret_params(modes)
                if params[0] != 0:
                    self.index = params[1]
                else:
                    self.index += 3
            elif fn == '06':
                params = self.interpret_params(modes)
                if params[0] == 0:
                    self.index = params[1]
                else:
                    self.index += 3
            elif fn == '07':
                params = self.interpret_params(modes)
                write_address = self.literal_params(modes)[2]
                if params[0] < params[1]:
                    self.memory[write_address] = 1
                else:
                    self.memory[write_address] = 0
                self.index += 4
            elif fn == '08':
                params = self.interpret_params(modes)
                write_address = self.literal_params(modes)[2]
                if params[0] == params[1]:
                    self.memory[write_address] = 1
                else:
                    self.memory[write_address] = 0
                self.index += 4
            elif fn == '09':
                params = self.interpret_params(modes)
                self.base += params[0]
                self.index += 2
            elif fn == '99':
                self.finished = True
                # print('\nOpcode Computer Finished')
                break
            else:
                print('Error')
                break
            
            

    
