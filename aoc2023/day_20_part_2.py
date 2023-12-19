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

    def state_value(self):
        return self.state.value


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

    def state_value(self):
        return tuple(pulse.value for _, pulse in sorted(self.state.items()))


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
    return min_button_presses(module_name_to_module)


def parse_module(line):
    name, recipient_names = line.split(" -> ")
    recipient_names = tuple(recipient_names.split(", "))
    if name[0] == "%":
        return FlipFlopModule(name[1:], recipient_names)
    if name[0] == "&":
        return ConjunctionModule(name[1:], recipient_names)
    return BroadcasterModule(name, recipient_names)


def min_button_presses(
    module_name_to_module,
):  # pylint: disable=too-complex, too-many-locals, too-many-branches
    # pylint: disable=line-too-long

    # Observe that there are four groups of ways to reach the 'rx' module from the button.
    # This can be verified manually, by drawing up a module schema graph.
    # Each of the four groups passes through exactly one broadcaster recipient ('tf', 'br', 'zn', 'nc'),
    # as well as through exactly one of the conjunction modules ('gt', 'vr', 'nl', 'lr')
    # that feed into the conjunction module ('jq') that ultimately feeds into the 'rx' module.
    # Assume that each of the four groups forms a cycle.
    # The problem boils down to finding the button press that will result in sending
    # a high pulse from 'gt', 'vr', 'nl', and 'lr' to 'jq' during the same pulse handling.
    # Each group is marked with a broadcast recipient as its name.

    # pylint: enable=line-too-long

    # establish pre-rx (i.e. 'jq') module
    penultimate_module_name = None
    for module in module_name_to_module.values():
        if "rx" in module.recipient_names:
            penultimate_module_name = module.name
            break

    # determine which modules pertain to which cycle
    # and which modules feed into the penultimate module
    cycles = {}
    penultimate_module_feeds = {}
    for start_module_name in module_name_to_module["broadcaster"].recipient_names:
        cycle_module_names = set()
        remaining = {start_module_name}
        while remaining:
            if (module_name := remaining.pop()) not in {"rx", penultimate_module_name}:
                cycle_module_names.add(module_name)
                recipient_names = set(
                    module_name_to_module[module_name].recipient_names
                )
                if penultimate_module_name in recipient_names:
                    penultimate_module_feeds[start_module_name] = module_name
                remaining.update(recipient_names.difference(cycle_module_names))
        cycles[start_module_name] = tuple(sorted(cycle_module_names))

    cycle_name_to_press_count_per_state = {
        cycle_name: {}
        for cycle_name in module_name_to_module["broadcaster"].recipient_names
    }
    CycleData = collections.namedtuple("CycleData", ("steps_to_loop", "loop_length"))
    cycle_data = {}

    button_presses = 1
    done = {
        cycle_name: False
        for cycle_name in module_name_to_module["broadcaster"].recipient_names
    }
    while not all(done.values()):
        queue = collections.deque(
            [Output(Input(PulseType.LOW, "button"), "broadcaster")]
        )
        while queue:
            input_, module_name = queue.pop()
            if module_name in module_name_to_module:
                for output in module_name_to_module[module_name].output(input_):
                    queue.appendleft(output)

            for cycle_name in module_name_to_module["broadcaster"].recipient_names:
                if (
                    module_name_to_module[penultimate_module_name].state[
                        penultimate_module_feeds[cycle_name]
                    ]
                    == PulseType.HIGH
                    and not done[cycle_name]
                ):
                    state_value = tuple(
                        module_name_to_module[module_name].state_value()
                        for module_name in cycles[cycle_name]
                    )
                    if (
                        cycle_name_to_press_count_per_state[cycle_name].get(
                            state_value, button_presses
                        )
                        != button_presses
                    ):
                        steps_to_loop = cycle_name_to_press_count_per_state[cycle_name][
                            state_value
                        ]
                        cycle_data[cycle_name] = CycleData(
                            steps_to_loop,
                            button_presses - steps_to_loop,
                        )
                        done[cycle_name] = True
                    elif (
                        button_presses
                        not in cycle_name_to_press_count_per_state[cycle_name].values()
                    ):
                        cycle_name_to_press_count_per_state[cycle_name][
                            state_value
                        ] = button_presses
        button_presses += 1

    # At this point cycle data looks like this:
    # {'br': (3889, 3889), 'tf': (3907, 3907), 'nc': (3911, 3911), 'zn': (4003, 4003)}
    # For each cycle it took exactly one whole loop length to enter the loop.
    # This is equivalent to having all 4 loops start on the very first step,
    # so in this particular case there's no need to apply the
    # Chinese remainder theorem to solve this linear system of modulo equations.
    # The solution is the least common multiple of loop lengths.

    return math.lcm(*(data.loop_length for data in cycle_data.values()))


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
