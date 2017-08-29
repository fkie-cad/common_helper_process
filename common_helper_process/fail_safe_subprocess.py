from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from signal import SIGKILL
import logging
import pexpect
from time import sleep


def execute_shell_command(shell_command, timeout=None):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :return: str
    """
    return execute_shell_command_get_return_code(shell_command, timeout=timeout)[0]


def execute_shell_command_get_return_code(shell_command, timeout=None):
    """
    Execute a shell command and return a tuple (program output, return code)
    Program ouput includes STDOUT and STDERR.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type: timeout: int
    :return: str, int
    """
    output = ""
    return_code = 1
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


def execute_interactive_shell_command(shell_command, timeout=60, inputs={}):
    """
    Execute an interactive shell command and return a tuple (program output, return code)
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :param timeout: kill process after timeout seconds
    :type timeout: int
    :param inputs: dictionary {'EXPECTED_CONSOLE_OUTPUT': 'DESIRED_INPUT'}
    :type inputs: dict
    :return: str, int
    """
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
