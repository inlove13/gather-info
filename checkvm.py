import sys
import ctypes
import os

if 'nt' in sys.builtin_module_names:
    # import windows registry.
    from _winreg import *
    # import windows ctypes windll...
    from ctypes import windll, WinError, create_string_buffer, byref, c_uint32, GetLastError

COMMAND = "cmd"
MANUFACTURER = "System Manufacturer"

def check_vm():
    """
    return str type of Virtual Machine information if it is virtual machine, otherwise False.
    """
    vmlists = ['VMware', 'Virtual Box', 'Hyper-V', 'Virtual PC', 'Xen', 'QEMU']
    try:
        registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = 'HARDWARE\DESCRIPTION\System\BIOS'
        rawkey = OpenKey(registry, key)
        i = 0
        while True:
            name, value, type = EnumValue(rawkey, i)
            if name == "SystemManufacturer":
                for vm in virtualmachine:
                    if vm.lower() in value.lower():
                        return value
                vmvalue = value
            # In case virtual machine name is not in vmlists.
            if name == "SystemFamily":
                if value == "Virtual Machine":
                    return vmvalue
            i += 1
    except EnvironmentError:
        # [Error 259] No more data is available
        pass

    data = shell_exec("SYSTEMINFO")
    for info in data:
        if info:
            line = info.split(":")
            key = line[0]
            value = line[1].lstrip() if len(line) > 1 else None
            if key == MANUFACTURER:
                for vm in virtualmachine:
                    if vm.lower() in value.lower():
                        return value
                break
    return False