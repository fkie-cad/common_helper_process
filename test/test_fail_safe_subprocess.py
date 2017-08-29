import unittest
from time import time
import os
from common_helper_files import get_dir_of_file

from common_helper_process import execute_shell_command, execute_shell_command_get_return_code, execute_interactive_shell_command
from common_helper_process.fail_safe_subprocess import _parse_inputs


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

    def test_execute_shell_command_time_out(self):
        start_time = time()
        output, rc = execute_shell_command_get_return_code('echo \'test 123\' && for i in {1..10}; do sleep 1; done', timeout=1)
        run_time = time() - start_time
        self.assertEqual(output, 'test 123\n\n\nERROR: execution timed out!', 'timeout message not added')
        self.assertEqual(rc, 1, 'return code not correct')
        self.assertGreater(5, run_time, "command not aborted")

    def test_parse_inputs(self):
        test_dict = {'a': 'a_out', 'b': 'b_out'}
        trigger, inputs = _parse_inputs(test_dict)
        self.assertEqual(trigger, ['a', 'b'])
        self.assertEqual(inputs, ['a_out', 'b_out'])

    def test_interactive_shell_command(self):
        script_path = os.path.join(get_dir_of_file(__file__), 'data/interactive.sh')
        expected_inputs = {'give me some input:\r\n': 'test_input_1', 'give me more:\r\n': 'test_input_2'}
        output, ret_code = execute_interactive_shell_command(script_path, inputs=expected_inputs, timeout=5)
        assert 'first=test_input_1' in output
        assert 'second=test_input_2' in output
        assert ret_code == 0

    def test_interactive_shell_command_none_correct_input(self):
        script_path = os.path.join(get_dir_of_file(__file__), 'data/interactive.sh')
        output, ret_code = execute_interactive_shell_command(script_path, timeout=2)
        assert 'give me some input' in output
        assert 'Error: Execution timed out!'
        assert ret_code > 0
