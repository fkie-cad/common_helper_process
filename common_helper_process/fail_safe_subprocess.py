import logging
from signal import SIGKILL
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, CalledProcessError
from time import sleep

import pexpect


def execute_shell_command(shell_command, timeout=None, check=False):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type: timeout: int, optional
    :param check: raise CalledProcessError if the return code is != 0
    :type: check: bool
    :return: str
    """
    output, return_code = execute_shell_command_get_return_code(shell_command, timeout=timeout)
    if check and return_code != 0:
        raise CalledProcessError(return_code, shell_command)
    return output


def execute_shell_command_get_return_code(shell_command, timeout=None):
    """
    Execute a shell command and return a tuple (program output, return code)
    Program output includes STDOUT and STDERR.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type: timeout: int, optional
    :return: str, int
    """
    pl = Popen(shell_command, shell=True, stdout=PIPE, stderr=STDOUT)
    try:
        output = pl.communicate(timeout=timeout)[0].decode('utf-8', errors='replace')
        return_code = pl.returncode
    except TimeoutExpired:
        logging.warning("Execution timeout!")
        pl.kill()
        output = pl.communicate()[0].decode('utf-8', errors='replace')
        output += "\n\nERROR: execution timed out!"
        return_code = 1
    return output, return_code


def execute_interactive_shell_command(shell_command, timeout=60, inputs=None):
    """
    Execute an interactive shell command and return a tuple (program output, return code)
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type timeout: int
    :param inputs: dictionary {'EXPECTED_CONSOLE_OUTPUT': 'DESIRED_INPUT'}
    :type inputs: dict, optional
    :return: str, int
    """
    if inputs is None:
        inputs = {}
    trigger, inputs = _parse_inputs(inputs)
    output = b''
    child = pexpect.spawn(shell_command)
    while True:
        try:
            i = child.expect(trigger, timeout=timeout)
            sleep(0.1)
            child.sendline(inputs[i])
            output += child.before + child.after
        except pexpect.TIMEOUT:
            child.kill(SIGKILL)
            output += child.before
            output += b'\n\nError: Execution timed out!'
            break
        except pexpect.EOF:
            output += child.before
            break
    child.close()
    output = output.decode('utf-8', errors='ignore')
    return_code = child.exitstatus if child.exitstatus is not None else 1
    return output, return_code


def _parse_inputs(input_dict):
    trigger = []
    inputs = []
    for item in sorted(input_dict.keys()):
        trigger.append(item)
        inputs.append(input_dict[item])
    return trigger, inputs
