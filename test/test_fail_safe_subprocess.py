import unittest

from common_helper_process import execute_shell_command
from common_helper_process.fail_safe_subprocess import execute_shell_command_get_return_code


class TestProcessHelper(unittest.TestCase):

    def test_execute_shell_command(self):
        result = execute_shell_command("echo 'test 123'")
        self.assertEqual(result, 'test 123\n', 'result not correct')

    def test_execute_shell_command_error(self):
        result = execute_shell_command("echo 'test 123' 1>&2 && exit 2")
        self.assertEqual(result, 'test 123\n', 'result not correct')

    def test_execute_shell_command_incl_rc(self):
        output, rc = execute_shell_command_get_return_code("echo 'test 123'")
        self.assertEqual(output, 'test 123\n', 'result not correct')
        self.assertEqual(rc, 0, 'return code not correct')

    def test_execute_shell_command_error_incl_rc(self):
        output, rc = execute_shell_command_get_return_code("echo 'test 123' 1>&2 && exit 2")
        self.assertEqual(output, 'test 123\n', 'result not correct')
        self.assertEqual(rc, 2, 'return code not correct')
