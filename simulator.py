"""
MIPS Simulator 0.2
Author: Brian Reily
Download: www.brianreily.com/media/code/simulator.py

License:  Use/Modify/Whatever, but credit would be sweet.

Classes:
Simulator -- Used to simulate MIPS code
"""
import re, sys

class Simulator:
    """ Simulates MIPS code.  Set verbose to True to get lots of
        output.  mem sets the memory size, the default being 1000
        bytes (250 words if you act like it's word-aligned).  pc sets
        the default start value.  Default is 0, in which case it
        starts at the first line.  Use run_lines([]) to run
        multiple lines of code.  Use run_line to run just one.
        Use get_register('$s3') to get the value there; likewise
        with get_data(address).  Use reset() to set everything to
        default and clear code, or rerun() to run the same instructions.

        .data directives are not supported yet, enter data
        manually before starting program.

        Available operations: syscall, j, b, jr, beq, bne, lw, sw,
        slt, slti, add, addi, sub, subi, and, andi, or, ori, sll,
        sllv, srl, srlv, div, mul, xor, xori, move"""

    def __init__(self, verbose=False, mem=1000, pc=0):
        self.verbose = verbose
        self.data = [0 for x in range(mem)]
        self.pc = pc
        self.instructions = []
        self.labels = {}
        self.registers = { '$0' : 0, '$at': 0, '$v0': 0, '$v1': 0,
                           '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
                           '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
                           '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
                           '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
                           '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
                           '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
                           '$gp': 0, '$sp': 0, '$s8': 0, '$ra': 0 }

        self.register_list = ['$0', '$at', '$v0', '$v1', '$a0', '$a1',
            '$a2', '$a3', '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6',
            '$t7', '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
            '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$s8', '$ra']

        self.function_lookup = {'add':'+',  'addi':'+',  'sub':'-',  'subi':'-',
                                'and':'&',  'andi':'&',   'or':'|',   'ori':'|',
                                'sll':'<<', 'sllv':'<<', 'srl':'>>', 'srlv':'>>',
                                'div':'/',   'mul':'*',  'xor':'^',  'xori':'^'  }

    def get_register(self, register):
        """Retrieve value of a register; Accepts $vo or $2."""
        try: return self.registers[register]
        except:
            try:
                register = register.strip('$')
                return self.registers[self.register_list[int(register)]]
            except:
                try: return self.registers[self.register_list[register]]
                except: return None

    def status(self):
        """Prints current status of the machine."""
        for register in self.register_list[:8]:
            print '%3s: %4s' %(register, self.registers[register]),
        print
        for register in self.register_list[8:16]:
            print '%3s: %4s' %(register, self.registers[register]),
        print
        for register in self.register_list[16:24]:
            print '%3s: %4s' %(register, self.registers[register]),
        print
        for register in self.register_list[24:32]:
            print '%3s: %4s' %(register, self.registers[register]),
        print
        for i, instruction in enumerate(self.instructions):
            print '%3s: %s' %(i, instruction)
        print 'Current PC: %s' %self.pc

    def run_lines(self, lines):
        """External method to run multiple lines."""
        lines = self.strip_comments(lines)
        self.instructions.extend(lines)
        self.find_labels(lines)
        while self.pc < len(self.instructions):
            print 'Running line %s: %s' %(self.pc, self.instructions[self.pc])
            self.execute(self.instructions[self.pc])
            self.pc += 1

    def run_line(self, line):
        """External method to execute one line."""
        try: line = self.strip_comments([line])[0]
        except:
            print "Can't execute comments"
            return
        self.execute(line)
        self.pc += 1
        self.instructions.append(line)

    def execute(self, line):
        """Internal method to execute a line of code."""
        if self.verbose: print '%s: %s' %(self.pc, line),
        if re.compile('^.*:').match(line): return
        elif re.compile('^syscall').match(line): self.syscall()
        elif re.compile('^(beq|bne)\s\$.{1,2},\s\$.{1,2},.*').match(line):
            self.branch(line)
        elif re.compile('^(j|b|jr|jal)\s.*').match(line): self.jump(line)
        elif re.compile('^(lw|sw)\s.*').match(line): self.load_store(line)
        elif re.compile('^(slt|slti)\s\$.{1,2},\s\$.{1,2},.*').match(line):
            self.set_less_than(line)
        elif re.compile('^move.*').match(line): self.move(line)
        elif re.compile('^[a-zA-Z]{2,4}\s\$.{1,2},\s\$.{1,2},.*').match(line):
            self.logical_arithmetic(line)

    def logical_arithmetic(self, line):
        """The majority of instructions: add, or, etc."""
        instr = re.compile('^[a-zA-Z]{2,4}\s').findall(line)[0].strip()
        func = self.function_lookup[instr]
        reg = [f.strip(' ,') for f in re.compile('\$.{1,2}').findall(line)]
        r1, r2 = reg[0], reg[1]
        if 'i' in instr[2:4] or instr in ('sll', 'srl'):
            imm = line.lstrip(instr + ' ').lstrip(r1 + ', ').lstrip(r2 + ', ')
            self.registers[r1] = eval(str(self.get_register(r2)) + func + imm)
            if self.verbose: print '\t# %s = %s %s %s = %s' %(r1,
                self.get_register(r2), func, imm, self.get_register(r1))
        else:
            r3 = reg[2]
            self.registers[r1] = eval(str(self.get_register(r2)) + func +
                                      str(self.get_register(r3)))
            if self.verbose: print '\t# %s = %s %s %s = %s' %(r1,
                self.get_register(r2), func, self.get_register(r3), self.get_register(r1))

    def move(self, line):
        """The move instruction."""
        reg = [f.strip(' ,') for f in re.compile('\$.{1,2}').findall(line)]
        r1, r2 = reg[0], reg[1]
        self.registers[r1] = self.get_register(r2)
        if self.verbose: print '\t# %s = %s' %(r1, self.get_register(r1))

    def set_less_than(self, line):
        """Set register to 1 if true."""
        reg = [f.strip(' ,') for f in re.compile('\$.{1,2}').findall(line)]
        if len(reg) == 3 and line[:3] == 'slt':
            r1, r2, r3 = reg[0], reg[1], reg[2]
            if self.get_register(r2) < self.get_register(r3):
                self.registers[r1] = 1
                if self.verbose: print '\t# %s < %s, so %s = 1' %(
                    self.get_register(r2), self.get_register(r3), r1)
            else:
                self.registers[r1] = 0
                if self.verbose: print '\t# %s !< %s, so %s = 0' %(
                    self.get_register(r2), self.get_register(r3), r1)
        elif len(reg) == 2 and line[:4] == 'slti':
            r1, r2 = reg[0], reg[1]
            line = line.lstrip('slti ').lstrip(r1 + ', ').lstrip(r2 + ', ')
            imm = int(line)
            if self.get_register(r2) < imm:
                self.registers[r1] = 1
                if self.verbose: print '\t# %s < %s, so %s = 1' %(
                    self.get_register(r2), imm, r1)
            else:
                self.registers[r1] = 0
                if self.verbose: print '\t# %s !< %s, so %s = 0' %(
                    self.get_register(r2), imm, r1)



    def load_store(self, line):
        """Handles lw and sw instructions."""
        part = line.lstrip('sw ').lstrip('lw ')
        reg = re.compile('(\$.{1,2})').findall(line)[0].strip(' ,')
        part = part.lstrip(reg + ', ')
        try: offset = int(re.compile('\d+\(').findall(line)[0].rstrip('('))
        except: offset = 0
        addr = re.compile('\(\$.{1,2}\)').findall(line)[0].strip('(').strip(')')
        addr = self.get_register(addr) + offset
        if line[:2] == 'sw':
            self.data[addr] = self.get_register(reg)
            if self.verbose: print '\t# Store %s in data[%s]' %(
                self.get_register(reg), addr)
        if line[:2] == 'lw':
            self.registers[reg] = self.data[addr]
            if self.verbose: print '\t# Load %s from data[%s]' %(
                self.get_register(reg), addr)

    def branch(self, line):
        """Handles beq and bne instructions."""
        reg = [r.strip(', ') for r in re.compile('\$.{1,2}').findall(line)]
        r1, r2 = reg[0], reg[1]
        label = line.lstrip('benq').lstrip(r1 + ', ').lstrip(r2 + ', ')
        if self.get_register(r1) == self.get_register(r2):
            if self.verbose: print '\t# %s == %s, ' %(r1, r2),
            if line[:3] == 'beq':
                try:
                    self.pc = self.labels[label]
                    if self.verbose: print 'branch to %s' %self.pc
                except:
                    if self.verbose: print 'can\'t find label'
            else:
                if self.verbose: print 'not branching'
        else:
            if self.verbose: print '\t# %s != %s, ' %(r1, r2),
            if line[:3] != 'bne':
                try:
                    self.pc = self.labels[label]
                    if self.verbose: print 'branch to %s' %self.pc
                except:
                    if self.verbose: print 'can\'t find label'
            else:
                if self.verbose: print 'not branching'

    def jump(self, line):
        """Handles jr, j and b instructions."""
        if re.compile('^jr\ +\$.*').match(line):
            register = line.lstrip('jr ')
            if self.verbose: print '\t# Old PC = %s, New PC = %s' %(
                self.pc, self.get_register(register))
            self.pc = self.get_register(register)
        elif re.compile('^jal .*').match(line):
            label = line[2:].strip()
            if label in self.labels:
                if self.verbose: print '\t# Old PC = %s' %self.pc,
                self.registers['$ra'] = pc + 1
                self.pc = self.labels[label]
                if self.verbose: print ', New PC = %s' %self.pc
            else: print '\t# Label not found, PC = %s' %self.pc
        else:
            label = line[2:].strip()
            if label in self.labels:
                if self.verbose: print '\t# Old PC = %s' %self.pc,
                self.pc = self.labels[label]
                if self.verbose: print ', New PC = %s' %self.pc
            else: print '\t# Label not found, PC = %s' %self.pc

    def syscall(self):
        """ Action based on value in $v0:
            1:  Print int in $a0
            5:  Read int into $v0
            10: Exit"""
        print 'syscall(%s)' %self.get_register('$v0')
        if self.verbose: print '\t# $v0 = %s, $a0 = %s' %(
            self.get_register('$v0'), self.get_register('$a0'))
        if self.get_register('$v0') == 1: print get_register('$a0')
        if self.get_register('$v0') == 5:
            self.registers['$v0'] = raw_input('read > ')
        if self.get_register('$v0') == 10: sys.exit()

    def rerun(self):
        """Rerun all instructions in memory."""
        lines = self.instructions
        self.pc = 0
        self.instructions = []
        self.run_lines(lines)

    def reset(self):
        """Reset everything to defaults."""
        self.instructions = []
        self.labels = {}
        self.pc = 0
        self.data = [0 for x in range(1000)]
        for r in self.register_list:
            self.registers[r] = 0

    def strip_comments(self, lines):
        """Strips out comments from a list of lines."""
        ret = []
        for line in lines:
            if '#' in line: line = line[:line.find('#')]
            line = line.strip().strip('\n')
            if len(line) < 2: continue
            ret.append(line)
        return ret

    def find_labels(self, lines):
        """Records all labels in program."""
        for i, line in enumerate(lines):
            if re.compile('^.*:').match(line):
                self.labels[line.strip().rstrip(':')] = i

    def __repr__(self):
        return '< Simulator -- PC: %s >' %self.pc
