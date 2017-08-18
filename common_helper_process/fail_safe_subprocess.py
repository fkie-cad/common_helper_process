from subprocess import Popen, PIPE, STDOUT


def execute_shell_command(shell_command):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :return: str
    """
    return execute_shell_command_get_return_code(shell_command)[0]


def execute_shell_command_get_return_code(shell_command):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :return: str, int
    """
    output = ""
    rc = 1
    with Popen(shell_command, shell=True, stdout=PIPE, stderr=STDOUT) as pl:
        output = pl.communicate()[0].decode('utf-8', errors='replace')
        rc = pl.returncode
    return output, rc
