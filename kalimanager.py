import os
import sys
import socket
from cli_fragments import CliFragments


def haltKali():
    if not isVmUp():
        io.notice("The virtual machine is not running.")
        return

    io.debug("Halting the virtual machine...")
    command = "vmrun -T fusion stop '/Users/sal/Virtual Machines.localized/Kali Linux.vmwarevm/Kali Linux.vmx'"
    os.system(command)

    io.debug("Waiting for the virtual machine unavailability...")
    while not isVmUp():
        continue

    io.success("The virtual machine has been halted.")


def runKali():
    if isVmUp():
        io.notice("The virtual machine is already running.")
        return

    io.debug("Booting the virtual machine...")
    command = "vmrun -T fusion start '/Users/sal/Virtual Machines.localized/Kali Linux.vmwarevm/Kali Linux.vmx' nogui 1> /dev/null"
    os.system(command)

    io.debug("Waiting for the virtual machine availability...")
    while not isVmUp():
        continue

    io.success("The virtual machine has been started.")


def statusKali():
    if isVmUp():
        io.success("The virtual machine is online.")
    else:
        io.error("The virtual machine is offline.")


def isVmUp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", 2222))
    sock.close()

    return result == 0


if __name__ == "__main__":

    io = CliFragments()

    if not len(sys.argv) > 1:
        io.text("Usage: kalimanager run|status|halt")
        exit(0)

    if sys.argv[1] == "halt":
        haltKali()
    elif sys.argv[1] == "run":
        runKali()
    elif sys.argv[1] == "status":
        statusKali()
    else:
        io.error("The command you provided does not exist.")
