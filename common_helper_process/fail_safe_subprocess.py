from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import logging


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
    rc = 1
    pl = Popen(shell_command, shell=True, stdout=PIPE, stderr=STDOUT)
    try:
        output = pl.communicate(timeout=timeout)[0].decode('utf-8', errors='replace')
        rc = pl.returncode
    except TimeoutExpired:
        logging.warning("Execution timeout!")
        pl.kill()
        output = pl.communicate()[0].decode('utf-8', errors='replace')
        output += "\n\nERROR: execution timed out!"
        rc = 1
    return output, rc
