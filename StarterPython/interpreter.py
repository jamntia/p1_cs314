import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Literal, Sequence

from data import Int64

### OPERANDS ###


class Variable(Enum):
    A, B, C, D, E, F = "abcdef"

    def __str__(self):
        return self.value

    @classmethod
    def is_variable(cls, value):
        return value in cls._value2member_map_


@dataclass
class VariableOperand:
    value: Variable


@dataclass
class ConstantOperand:
    value: int


@dataclass
class RegisterOperand:
    value: int


Operand = VariableOperand | ConstantOperand | RegisterOperand
OperandType = Literal["variable", "constant", "register"]


def parse_operand(operand_type: OperandType, operand: str) -> Operand:
    match operand_type:
        case "constant":
            assert operand[0] == "#", "expected constant"
            return ConstantOperand(int(operand[1:]))
        case "register":
            assert operand[0] == "r", "expected register"
            return RegisterOperand(int(operand[1:]))
        case "variable":
            assert Variable.is_variable(operand), "expected variable"
            return VariableOperand(Variable(operand))


### MACHINE ###


class IO(ABC):
    @abstractmethod
    def read(self, prompt: str) -> int:
        pass

    @abstractmethod
    def write(self, text: str):
        pass


class StdIO(IO):
    def read(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Please enter a valid integer.")

    def write(self, text: str):
        print(text)


InstructionHandler = Callable[["Machine", tuple[int | Variable, ...]], None]


@dataclass
class Instruction:
    signature: list[OperandType]
    handler: InstructionHandler


class Machine:  # pyright: ignore
    InstructionSet = dict[str, Instruction]()

    def __init__(self, io: IO):
        self.io = io
        self.variables = defaultdict[Variable, Int64](Int64)
        self.registers = defaultdict[int, Int64](Int64)
        self.instruction_count = 0

    def execute(self, line: str):
        line = line.strip()
        if not line:
            return

        opcode, *args = line.split()
        assert opcode in Machine.InstructionSet, f"Unknown opcode {opcode}"
        instruction = Machine.InstructionSet[opcode]

        operands = [
            parse_operand(operand_type, args[inx])
            for inx, operand_type in enumerate(instruction.signature)
        ]

        # registers = [op.value for op in operands if isinstance(op, RegisterOperand)]
        # duplicates = [r for r, c in Counter(registers).items() if c > 1]
        # assert not duplicates, f"Duplicate register operands: {duplicates}"

        instruction.handler(self, tuple(operand.value for operand in operands))  # pyright: ignore

        self.instruction_count += 1


def Opcode(name: str, signature: Sequence[OperandType]):
    def decorator(handler):
        Machine.InstructionSet[name] = Instruction(list(signature), handler)
        return handler

    return decorator


### INSTRUCTION SET ###


class Machine(Machine):
    @Opcode("LOADI", ("register", "constant"))
    def op_loadi(self, ops):
        self.registers[ops[0]] = Int64(ops[1])

    @Opcode("LOAD", ("register", "variable"))
    def op_load(self, ops):
        self.registers[ops[0]] = self.variables[ops[1]]

    @Opcode("STORE", ("variable", "register"))
    def op_store(self, ops):
        self.variables[ops[0]] = self.registers[ops[1]]

    @Opcode("ADD", ("register", "register", "register"))
    def op_add(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] + self.registers[ops[2]]

    @Opcode("SUB", ("register", "register", "register"))
    def op_sub(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] - self.registers[ops[2]]

    @Opcode("MUL", ("register", "register", "register"))
    def op_mul(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] * self.registers[ops[2]]

    @Opcode("AND", ("register", "register", "register"))
    def op_and(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] & self.registers[ops[2]]

    @Opcode("OR", ("register", "register", "register"))
    def op_or(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] | self.registers[ops[2]]

    @Opcode("XOR", ("register", "register", "register"))
    def op_xor(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] ^ self.registers[ops[2]]

    @Opcode("LS", ("register", "register", "register"))
    def op_ls(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] << self.registers[ops[2]]

    @Opcode("RS", ("register", "register", "register"))
    def op_rs(self, ops):
        self.registers[ops[0]] = self.registers[ops[1]] >> self.registers[ops[2]]

    @Opcode("NOT", ("register", "register"))
    def op_not(self, ops):
        self.registers[ops[0]] = ~self.registers[ops[1]]

    @Opcode("READ", ("variable",))
    def op_read(self, ops):
        self.variables[ops[0]] = Int64(self.io.read(f'enter value for "{ops[0]}": '))

    @Opcode("WRITE", ("variable",))
    def op_write(self, ops):
        self.io.write(f"tinyL>> {ops[0]} = {int(self.variables[ops[0]])}")


if __name__ == "__main__":
    print("""

    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣀⣀⠀⠀⣀⡠⠴⠒⠚⠉⠉⠓⠒⠦⣄⣶⠒⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡷⢬⣉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠠⡌⠻⣧⢻⣧⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣖⠗⡋⢹⠀⠀⢰⡄⠀⠀⢸⣷⡀⠀⣠⠽⣆⢼⣇⢻⣸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⣡⣶⢋⡏⠙⢢⣏⣇⠀⠀⠈⣇⡵⡏⠀⠀⢹⡏⢾⣿⠃⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢿⢻⣏⣿⡇⡄⣾⠀⠹⡄⠄⠀⡇⠀⠹⣤⠈⠹⣿⣾⢸⠀⢘⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣯⣿⣽⣿⣷⢸⡗⠦⣄⡹⣼⣄⣿⣴⠛⠹⡄⡇⣿⣿⠾⠚⢹⢿⢽⣽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣞⣾⣿⢿⣯⢻⢻⡴⠞⠁⠈⠻⣿⣌⡉⠓⣿⣰⡿⠀⠀⠀⠸⡜⡾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣡⠊⢸⣹⠁⠈⠙⣾⡄⠁⠀⢰⠛⠉⠉⠉⢳⣀⣿⣿⠃⠀⠀⣀⣀⣧⣿⡞⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⡴⠁⠀⠸⢿⣤⣤⣤⣹⣿⣷⣶⣾⣷⣶⣶⣺⣋⣽⣿⣷⠶⠟⠛⠋⢧⠀⠀⠸⡜⣷⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⠁⡰⠁⠀⠀⢠⡿⠀⠀⠀⠉⠉⠉⠙⢻⡟⣹⣿⠃⣿⠋⠁⠀⠀⠀⠀⠀⠸⡄⠀⠀⢣⠹⣧⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⡀⢠⠇⠀⠀⢠⡿⠁⠀⠀⠀⠀⣤⣶⡴⠚⢻⠡⣸⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠸⡄⢻⣇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⣼⠁⢸⠀⠀⠀⣾⠃⠀⠀⠀⠀⠀⢻⣿⣧⣀⣬⠋⠁⠀⣠⣿⣶⣆⠀⠀⠀⠀⠀⡇⠀⠀⠀⡇⠈⣿⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣸⣿⠀⡇⠀⢰⣸⡟⠀⠀⠀⣀⣠⠴⠚⣟⣻⣧⣯⣗⣤⣾⣿⣿⡿⠋⠀⠀⠀⠀⣸⣤⠀⠀⠀⡇⡆⢻⠃⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⢸⡀⣇⠀⣸⣿⡁⠀⣾⣻⡁⣀⣤⣶⠟⠋⠉⠛⢿⣋⣻⡏⠉⠀⠀⠀⠀⠀⢰⣿⡇⠀⠀⠀⣷⡇⣸⡄⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠇⠀⢧⢸⠀⣿⡿⠇⠀⠈⠛⠛⠋⠉⠀⠀⠀⠀⠀⡟⠀⣿⠇⠀⠀⠀⠀⠀⢠⣿⣿⡇⠀⠀⣰⡿⣧⣿⠃⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣄⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⣿⠀⠀⠀⠀⠀⠀⣸⡿⢸⠁⢠⣾⠋⢰⣿⡏⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣶⣶⡿⠀⠀⠀⠀⠀⠀⠉⠁⢸⣶⡟⠁⠀⠾⠟⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)
    print("--- Hatsune Miku's Modified RISC Simulator! ---")
    print("")
    if len(sys.argv) < 2:
        print("Missing Input File!")
        print("Usage: ./sim.py <input.risc>")
        print()
        print("Supported Instructions:")
        for opcode, instruction in Machine.InstructionSet.items():
            print(
                f"  {opcode.ljust(6)} {' '.join(f'<{i}>' for i in instruction.signature)}"
            )
        exit(1)

    machine = Machine(StdIO())
    with open(sys.argv[1], "r") as file:
        for inx, line in enumerate(file):
            try:
                machine.execute(line)
            except Exception as e:
                print(f"Error running line {inx + 1}:")
                print(line)
                raise e

    print(f"Ran {machine.instruction_count} instructions")
