import unittest

from common_helper_process import execute_shell_command


class Test(unittest.TestCase):

    def test_execute_shell_command(self):
        result = execute_shell_command("echo 'test 123'")
        self.assertEqual(result, 'test 123\n', 'result not correct')

    def test_execute_shell_command_error(self):
        result = execute_shell_command("echo 'test 123' 1>&2 && exit 2")
        self.assertEqual(result, 'test 123\n', 'result not correct')
