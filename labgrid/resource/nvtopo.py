import attr

from ..factory import target_factory
from .common import NetworkResource, Resource


@target_factory.reg_resource
@attr.s(eq=False)
class NVIDIATopoInterface(Resource):
    """This resource describes a NVIDIA Tegra On-Platform Operator interface.

    Args:
        serial (str): Serial of debug board
        index (int): Instance of debug board if there is more than one with the same serial, starts with 0"""

    serialno = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    index = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
    target = attr.ib(default="topo", validator=attr.validators.in_(["topo", "pm342"]))
    variant = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@target_factory.reg_resource
@attr.s(eq=False)
class NetworkNVIDIATopoInterface(NetworkResource):
    """ "This resource describes a remote NVIDIA Tegra On-Platform Operator interface.

    Args:
        serial (str): Serial of debug board
        index (int): Instance of debug board if there is more than one with the same serial, starts with 0"""

    serialno = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    index = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
    target = attr.ib(default="topo", validator=attr.validators.in_(["topo", "pm342"]))
    variant = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
