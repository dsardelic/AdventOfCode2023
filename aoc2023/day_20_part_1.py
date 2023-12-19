import abc
import collections
import dataclasses
import enum
import math

PulseType = enum.Enum("PulseType", ["LOW", "HIGH"])

StateType = enum.Enum("StateType", ["OFF", "ON"])

Input = collections.namedtuple("Input", ("pulse", "sender_name"))

Output = collections.namedtuple("Message", ("input_", "recipient_name"))


@dataclasses.dataclass
class AbstractModule(abc.ABC):
    name: str
    recipient_names: tuple[str]

    @abc.abstractmethod
    def output(self, input_):
        ...


@dataclasses.dataclass
class BroadcasterModule(AbstractModule):
    def output(self, _):
        return (
            Output(Input(PulseType.LOW, self.name), recipient_name)
            for recipient_name in self.recipient_names
        )


@dataclasses.dataclass
class FlipFlopModule(AbstractModule):
    state: StateType = StateType.OFF

    def output(self, input_):
        if input_.pulse == PulseType.LOW:
            match self.state:
                case StateType.OFF:
                    self.state = StateType.ON
                    output_pulse = PulseType.HIGH
                case StateType.ON:
                    self.state = StateType.OFF
                    output_pulse = PulseType.LOW
            return (
                Output(Input(output_pulse, self.name), recipient_name)
                for recipient_name in self.recipient_names
            )
        return tuple()


@dataclasses.dataclass
class ConjunctionModule(AbstractModule):
    state: dict[str, PulseType] = dataclasses.field(default_factory=dict)

    def output(self, input_):
        pulse, sender_name = input_
        self.state[sender_name] = pulse
        output_pulse = (
            PulseType.LOW
            if all(value == PulseType.HIGH for value in self.state.values())
            else PulseType.HIGH
        )
        return (
            Output(Input(output_pulse, self.name), recipient_name)
            for recipient_name in self.recipient_names
        )


def solution(input_rel_uri):
    module_name_to_module = {}
    with open(input_rel_uri, encoding="utf-8") as ifile:
        for line in ifile:
            module = parse_module(line.strip("\n"))
            module_name_to_module[module.name] = module
    for sender_name, sender in module_name_to_module.items():
        for recipient_name in sender.recipient_names:
            if recipient_name in module_name_to_module and isinstance(
                module_name_to_module[recipient_name], ConjunctionModule
            ):
                module_name_to_module[recipient_name].state[sender_name] = PulseType.LOW
    return count_propagated_pulses(module_name_to_module)


def parse_module(line):
    name, recipient_names = line.split(" -> ")
    recipient_names = tuple(recipient_names.split(", "))
    if name[0] == "%":
        return FlipFlopModule(name[1:], recipient_names)
    if name[0] == "&":
        return ConjunctionModule(name[1:], recipient_names)
    return BroadcasterModule(name, recipient_names)


def count_propagated_pulses(module_name_to_module):
    pulse_distribution = {pulse_type: 0 for pulse_type in PulseType}
    for _ in range(1000):
        queue = collections.deque(
            [Output(Input(PulseType.LOW, "button"), "broadcaster")]
        )
        while queue:
            input_, module_name = queue.pop()
            pulse_distribution[input_.pulse] += 1
            if module_name in module_name_to_module:
                for output in module_name_to_module[module_name].output(input_):
                    queue.appendleft(output)
    return math.prod(pulse_distribution.values())


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}_example1.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
