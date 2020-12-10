from __future__ import annotations

import sys
from bisect import bisect_right
from dataclasses import dataclass, field
import re
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple


INSTRUCTION_RE = re.compile(r"(?P<instruction>[a-z]{3}) (?P<argument>[+-]\d+)")


@dataclass
class Program:
    instructions: List[Instruction]
    accumulator: int = 0
    instruction_pointer: int = 0
    seen_instructions: Set[int] = field(default_factory=set)

    @staticmethod
    def from_input(lines: Iterable[str]) -> Program:
        return Program(instructions=[Instruction.from_line(line) for line in lines])

    def next(self) -> None:
        self.seen_instructions.add(self.instruction_pointer)
        self.instructions[self.instruction_pointer].execute(self)
        self.instruction_pointer += 1

    @property
    def is_stuck(self) -> bool:
        return self.instruction_pointer in self.seen_instructions

    @property
    def finished(self) -> bool:
        return self.instruction_pointer >= len(self.instructions)

    def execute(self) -> bool:
        while not self.is_stuck:
            if self.finished:
                return True
            self.next()
        return False


@dataclass
class Instruction:
    argument: int

    def execute(self, program: Program) -> None:
        pass

    @staticmethod
    def from_line(line: str) -> Instruction:
        if not (match := INSTRUCTION_RE.match(line)):
            raise Exception(f"Invalid Instruction Line: {line}")
        argument = int(match["argument"])
        if (instruction := match["instruction"]) == "nop":
            return Noop(argument)
        elif instruction == "jmp":
            return Jump(argument)
        elif instruction == "acc":
            return Accumulate(argument)
        else:
            raise Exception(f"Invalid Instruction: {instruction}")


class Noop(Instruction):
    pass


class Accumulate(Instruction):
    def execute(self, program: Program) -> None:
        program.accumulator += self.argument


class Jump(Instruction):
    def execute(self, program: Program) -> None:
        program.instruction_pointer += self.argument - 1


def flip_candidates(
    candidates: List[Tuple[int, int]], original_instructions: Set[int]
) -> Iterator[Tuple[int, Instruction]]:
    for idx, argument in candidates:
        if idx in original_instructions and idx + 1 not in original_instructions:
            yield (idx, Jump(argument))


def fix_stuck_program(program: Program) -> Optional[Program]:
    jump_candidates = []
    for idx, inst in enumerate(program.instructions):
        if isinstance(inst, Noop):
            jump_candidates.append((idx, inst.argument))
        elif isinstance(inst, Jump):
            jump_candidates.append((idx, 1))
    candidates = flip_candidates(jump_candidates, program.seen_instructions.copy())
    fixed_instruction: Optional[Tuple[int, Instruction]] = None
    while not program.execute():
        fixed_instruction = next(candidates, None)
        if not fixed_instruction:
            break
        program.instruction_pointer = (
            fixed_instruction[0] + fixed_instruction[1].argument
        )
    if not program.finished or not fixed_instruction:
        return None
    fixed_instructions = program.instructions.copy()
    fixed_instructions[fixed_instruction[0]] = fixed_instruction[1]
    return Program(instructions=fixed_instructions)


def main() -> None:
    program = Program.from_input(open("input.txt", "r").readlines())
    program.execute()
    print(f"Part 1: {program.accumulator}")
    fixed_program = fix_stuck_program(program)
    fixed_program.execute()
    print(f"Part 2: {fixed_program.accumulator}")


if __name__ == "__main__":
    main()
