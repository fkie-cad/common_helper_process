from subprocess import Popen, PIPE, STDOUT


def execute_shell_command(shell_command):
    """
    Execute a shell command and return STDOUT and STDERR in one combined result string.
    This function shall not raise any errors

    :param shell_command: command to execute
    :type shell_command: str
    :return: str
    """
    output = ""
    with Popen(shell_command, shell=True, stdout=PIPE, stderr=STDOUT) as pl:
        output = pl.communicate()[0].decode('utf-8', errors='replace')
    return output
