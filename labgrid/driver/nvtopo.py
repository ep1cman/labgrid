import subprocess

import attr

from ..factory import target_factory
from ..protocol import PowerProtocol, ResetProtocol
from ..step import step
from .common import Driver


@target_factory.reg_driver
@attr.s(eq=False)
class NVIDIATopoDriver(Driver, PowerProtocol, ResetProtocol):
    """NVIDIATopoDriver - Driver using NVIDIA Tegra On-Platform Operator to control a target's power

    https://docs.nvidia.com/jetson/archives/r36.4.3/DeveloperGuide/AT/BoardAutomation.html"""

    bindings = {"interface": {"NVIDIATopoInterface", "NetworkNVIDIATopoInterface"}}

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        if self.target.env:
            self.tool = self.target.env.config.get_tool("boardctl")
        else:
            self.tool = "boardctl"
        self._base_command = [*self.interface.command_prefix, self.tool, "-t", self.interface.interface_type]
        if self.interface.serialno is not None:
            self._base_command += ["-s", self.interface.serialno]
        if self.interface.index is not None:
            self._base_command += ["-i", str(self.interface.index)]
        if self.interface.variant is not None:
            self._base_command += ["-v", str(self.interface.variant)]

    @Driver.check_active
    @step()
    def on(self):
        (subprocess.run([*self._base_command, "power_on"], check=True, timeout=30),)

    @Driver.check_active
    @step()
    def off(self):
        subprocess.run([*self._base_command, "power_off"], check=True, timeout=30)

    @Driver.check_active
    @step()
    def cycle(self):
        self.off()
        # No neet to wait here since this is already done within `boardctl`
        self.on()

    @Driver.check_active
    @step()
    def get(self):
        r = subprocess.run([*self._base_command, "status"], check=True, timeout=30, text=True, capture_output=True)
        return "VDD_CPU is on" in r.stdout

    @Driver.check_active
    @step()
    def reset(self, mode=None):
        if mode is None:  # Default to soft reset using reset button
            subprocess.run([*self._base_command, "reset"], check=True, timeout=30)
        elif mode == "hard":
            self.cycle()
        elif mode == "recovery":
            subprocess.run([*self._base_command, "recovery"], check=True, timeout=30)

        else:
            raise ValueError(f"Unknown reset mode: {mode}")
