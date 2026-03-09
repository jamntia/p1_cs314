import sys
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import TextIO
from data import Int64

"""
          CS314 Project 1. Python Starter written by Winston Li

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

"""


# ---------------------------------------------------------------------------
# AST node types
# ---------------------------------------------------------------------------

@dataclass
class NumberNode:
    value: int          # 64-bit signed Python int


@dataclass
class VariableNode:
    name: str           # 'a'–'f'


@dataclass
class BinOpNode:
    op: str             # '+' '-' '*' '&' '|' '^' '<' '>'
    left:  object
    right: object


@dataclass
class UnaryOpNode:
    op: str             # '~'
    operand: object


@dataclass
class AssignNode:
    var: str
    expr: object


@dataclass
class ReadNode:
    var: str


@dataclass
class WriteNode:
    var: str


# ---------------------------------------------------------------------------
# Opcode enum (kept for compatibility; unused by new emitter)
# ---------------------------------------------------------------------------

class Opcode(Enum):
    (
        LOAD,
        LOADI,
        STORE,
        ADD,
        SUB,
        MUL,
        OR,
        AND,
        XOR,
        LS,
        RS,
        NOT,
        READ,
        WRITE,
    ) = range(14)


# ---------------------------------------------------------------------------
# Optimizer (Pass 2): constant folding, algebraic simplification, DCE
# ---------------------------------------------------------------------------

class Optimizer:
    def optimize(self, stmts: list) -> list:
        changed = True
        while changed:
            stmts, c1 = self._const_fold_stmts(stmts)
            stmts, c2 = self._simplify_stmts(stmts)
            stmts, c3 = self._dce(stmts)
            changed = c1 or c2 or c3
        return stmts

    # -- Constant folding --------------------------------------------------

    def _eval(self, op, a, b):
        a64, b64 = Int64(a), Int64(b)
        match op:
            case '+': return int(a64 + b64)
            case '-': return int(a64 - b64)
            case '*': return int(a64 * b64)
            case '&': return int(a64 & b64)
            case '|': return int(a64 | b64)
            case '^': return int(a64 ^ b64)
            case '<': return int(a64 << b64)
            case '>': return int(a64 >> b64)

    def _fold_expr(self, node):
        """Returns (new_node, changed_bool)."""
        if isinstance(node, (NumberNode, VariableNode)):
            return node, False
        if isinstance(node, UnaryOpNode):
            new_op, c = self._fold_expr(node.operand)
            if isinstance(new_op, NumberNode):
                return NumberNode(int(~Int64(new_op.value))), True
            return UnaryOpNode(node.op, new_op), c
        if isinstance(node, BinOpNode):
            new_left, cl = self._fold_expr(node.left)
            new_right, cr = self._fold_expr(node.right)
            if isinstance(new_left, NumberNode) and isinstance(new_right, NumberNode):
                result = self._eval(node.op, new_left.value, new_right.value)
                return NumberNode(result), True
            return BinOpNode(node.op, new_left, new_right), cl or cr
        return node, False

    def _const_fold_stmts(self, stmts):
        new_stmts = []
        changed = False
        for stmt in stmts:
            if isinstance(stmt, AssignNode):
                new_expr, c = self._fold_expr(stmt.expr)
                new_stmts.append(AssignNode(stmt.var, new_expr))
                changed = changed or c
            else:
                new_stmts.append(stmt)
        return new_stmts, changed

    # -- Algebraic simplification -----------------------------------------

    def _apply_rule(self, node):
        """Apply one algebraic simplification rule. Returns (new_node, changed)."""
        op, l, r = node.op, node.left, node.right
        zero = lambda n: isinstance(n, NumberNode) and n.value == 0
        one  = lambda n: isinstance(n, NumberNode) and n.value == 1
        neg1 = lambda n: isinstance(n, NumberNode) and n.value == -1

        if op == '^' and l == r:                        return NumberNode(0), True
        if op == '&' and (zero(l) or zero(r)):          return NumberNode(0), True
        if op == '*' and (zero(l) or zero(r)):          return NumberNode(0), True
        if op == '+' and zero(l):                       return r, True
        if op == '+' and zero(r):                       return l, True
        if op == '-' and zero(r):                       return l, True
        if op == '*' and one(l):                        return r, True
        if op == '*' and one(r):                        return l, True
        if op == '|' and zero(l):                       return r, True
        if op == '|' and zero(r):                       return l, True
        if op == '^' and zero(l):                       return r, True
        if op == '^' and zero(r):                       return l, True
        if op == '&' and neg1(l):                       return r, True
        if op == '&' and neg1(r):                       return l, True
        return node, False

    def _simplify_expr(self, node):
        if isinstance(node, (NumberNode, VariableNode)):
            return node, False
        if isinstance(node, UnaryOpNode):
            new_op, c = self._simplify_expr(node.operand)
            return UnaryOpNode(node.op, new_op), c
        if isinstance(node, BinOpNode):
            new_left, cl = self._simplify_expr(node.left)
            new_right, cr = self._simplify_expr(node.right)
            new_node = BinOpNode(node.op, new_left, new_right)
            simplified, c = self._apply_rule(new_node)
            return simplified, cl or cr or c
        return node, False

    def _simplify_stmts(self, stmts):
        new_stmts = []
        changed = False
        for stmt in stmts:
            if isinstance(stmt, AssignNode):
                new_expr, c = self._simplify_expr(stmt.expr)
                new_stmts.append(AssignNode(stmt.var, new_expr))
                changed = changed or c
            else:
                new_stmts.append(stmt)
        return new_stmts, changed

    # -- Dead-code elimination --------------------------------------------

    def _vars_in(self, expr) -> set:
        if isinstance(expr, VariableNode):  return {expr.name}
        if isinstance(expr, NumberNode):    return set()
        if isinstance(expr, UnaryOpNode):   return self._vars_in(expr.operand)
        if isinstance(expr, BinOpNode):     return self._vars_in(expr.left) | self._vars_in(expr.right)
        return set()

    def _dce(self, stmts):
        live = set()
        kept = []
        changed = False
        for stmt in reversed(stmts):
            if isinstance(stmt, WriteNode):
                live.add(stmt.var)
                kept.append(stmt)
            elif isinstance(stmt, ReadNode):
                live.discard(stmt.var)
                kept.append(stmt)
            elif isinstance(stmt, AssignNode):
                if stmt.var in live:
                    live.discard(stmt.var)
                    live |= self._vars_in(stmt.expr)
                    kept.append(stmt)
                else:
                    changed = True   # dropped a dead assignment
            else:
                kept.append(stmt)
        kept.reverse()
        return kept, changed


# ---------------------------------------------------------------------------
# CodeEmitter (Pass 3): walk AST → RISC instructions, with inline CSE
# ---------------------------------------------------------------------------

OPCODE = {
    '+': 'ADD', '-': 'SUB', '*': 'MUL',
    '&': 'AND', '|': 'OR',  '^': 'XOR',
    '<': 'LS',  '>': 'RS',
}


class CodeEmitter:
    def __init__(self, out):
        self.out = out
        self.reg_count = 0
        self.var_ver = {v: 0 for v in 'abcdef'}   # version per variable
        self.cse = {}                               # expr_key → register int

    def _new_reg(self):
        self.reg_count += 1
        return self.reg_count

    def _key(self, node):
        """Hashable key encoding variable versions for CSE validity."""
        if isinstance(node, NumberNode):    return ('n', node.value)
        if isinstance(node, VariableNode):  return ('v', node.name, self.var_ver[node.name])
        if isinstance(node, BinOpNode):     return ('b', node.op, self._key(node.left), self._key(node.right))
        if isinstance(node, UnaryOpNode):   return ('u', self._key(node.operand))

    def emit_expr(self, node) -> int:
        key = self._key(node)
        if key in self.cse:
            return self.cse[key]        # CSE hit — reuse register

        if isinstance(node, NumberNode):
            r = self._new_reg()
            self.out.write(f"LOADI r{r} #{node.value}\n")
        elif isinstance(node, VariableNode):
            r = self._new_reg()
            self.out.write(f"LOAD r{r} {node.name}\n")
        elif isinstance(node, BinOpNode):
            lr = self.emit_expr(node.left)
            rr = self.emit_expr(node.right)
            r = self._new_reg()
            self.out.write(f"{OPCODE[node.op]} r{r} r{lr} r{rr}\n")
        elif isinstance(node, UnaryOpNode):
            or_ = self.emit_expr(node.operand)
            r = self._new_reg()
            self.out.write(f"NOT r{r} r{or_}\n")

        self.cse[key] = r
        return r

    def emit_stmt(self, stmt):
        if isinstance(stmt, ReadNode):
            self.out.write(f"READ {stmt.var}\n")
            self.var_ver[stmt.var] += 1   # invalidate CSE entries via version
        elif isinstance(stmt, WriteNode):
            self.out.write(f"WRITE {stmt.var}\n")
        elif isinstance(stmt, AssignNode):
            r = self.emit_expr(stmt.expr)
            self.out.write(f"STORE {stmt.var} r{r}\n")
            self.var_ver[stmt.var] += 1

    def emit_program(self, stmts):
        for s in stmts:
            self.emit_stmt(s)


# ---------------------------------------------------------------------------
# Parser (Pass 1): recursive-descent LL(1), builds AST nodes
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, buffer: deque[str], out: TextIO):
        self.out = out
        self.buffer = buffer
        self.token = self.buffer.popleft()
        self.register_number = 0

    def next_token(self) -> None:
        assert self.buffer, "End of program input"
        print(self.token, end=" ")
        if self.token == ";":
            print()
        self.token = self.buffer.popleft()
        if self.token == "!":
            print("!")

    def next_register(self) -> int:
        self.register_number += 1
        return self.register_number

    def emit_instruction(
        self, opcode: Opcode, operand1: int, operand2: int = -1, operand3: int = -1
    ):
        match opcode:
            case Opcode.LOAD:
                self.out.write(f"LOAD r{operand1} {chr(operand2)}")
            case Opcode.LOADI:
                self.out.write(f"LOADI r{operand1} #{operand2}")
            case Opcode.STORE:
                self.out.write(f"STORE {chr(operand1)} r{operand2}")
            case Opcode.ADD:
                self.out.write(f"ADD r{operand1} r{operand2} r{operand3}")
            case Opcode.SUB:
                self.out.write(f"SUB r{operand1} r{operand2} r{operand3}")
            case Opcode.MUL:
                self.out.write(f"MUL r{operand1} r{operand2} r{operand3}")
            case Opcode.OR:
                self.out.write(f"OR r{operand1} r{operand2} r{operand3}")
            case Opcode.AND:
                self.out.write(f"AND r{operand1} r{operand2} r{operand3}")
            case Opcode.XOR:
                self.out.write(f"XOR r{operand1} r{operand2} r{operand3}")
            case Opcode.LS:
                self.out.write(f"LS r{operand1} r{operand2} r{operand3}")
            case Opcode.RS:
                self.out.write(f"RS r{operand1} r{operand2} r{operand3}")
            case Opcode.NOT:
                self.out.write(f"NOT r{operand1} r{operand2}")
            case Opcode.READ:
                self.out.write(f"READ {chr(operand1)}")
            case Opcode.WRITE:
                self.out.write(f"WRITE {chr(operand1)}")
        self.out.write("\n")

    ##################################################
    # Definitions for recursive descent LL(1) Parser #
    ##################################################

    def digit(self) -> NumberNode:
        assert self.token.isnumeric(), "Expected digit"
        value = int(self.token)
        self.next_token()
        return NumberNode(value)

    def variable(self) -> VariableNode:
        name = self.token
        self.next_token()
        return VariableNode(name)

    def expr(self) -> object:
        match self.token:
            case "+" | "-" | "*" | "&" | "|" | "^" | "<" | ">":
                op = self.token
                self.next_token()
                left = self.expr()
                right = self.expr()
                return BinOpNode(op, left, right)
            case "~":
                self.next_token()
                operand = self.expr()
                return UnaryOpNode("~", operand)
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                return self.digit()
            case "a" | "b" | "c" | "d" | "e" | "f":
                return self.variable()
            case _:
                raise Exception(f"Unknown symbol {self.token}")

    def assign(self) -> AssignNode:
        var = self.token
        self.next_token()               # consume var
        self.check_token("=")
        self.next_token()               # consume '='
        return AssignNode(var, self.expr())

    def read(self) -> ReadNode:
        self.next_token()               # consume '$'
        var = self.token
        self.next_token()
        return ReadNode(var)

    def print(self) -> WriteNode:
        self.next_token()               # consume '#'
        var = self.token
        self.next_token()
        return WriteNode(var)

    def stmt(self) -> object:
        if   self.token == "$": return self.read()
        elif self.token == "#": return self.print()
        else:                   return self.assign()

    def morestmts(self) -> list:
        if self.token == ";":
            self.next_token()           # consume ';'
            return self.stmtlist()
        return []                       # lookahead is '!'

    def stmtlist(self) -> list:
        return [self.stmt()] + self.morestmts()

    def program(self) -> None:
        stmts = self.stmtlist()
        self.check_token("!")
        stmts = Optimizer().optimize(stmts)
        CodeEmitter(self.out).emit_program(stmts)

    def check_token(self, tok):
        assert tok == self.token, f"Expected '{tok}' but received '{self.token}'"


if __name__ == "__main__":
    print("""------------------------------------------------
|       CS314 Python Compiler for tinyL        |
------------------------------------------------""")

    assert len(sys.argv) == 3, (
        "Incorrect Usage: python compiler.py <in.tinyL> <out.risc>"
    )

    with open(sys.argv[1], "r") as file:
        tokens = deque([i for i in file.read() if not i.isspace()])

    with open(sys.argv[2], "w") as out:
        parser = Parser(tokens, out)
        parser.program()

    print(f'\nCode written to "{sys.argv[2]}".\n')
