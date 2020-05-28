import os
import sys
import tempfile
from unittest.mock import patch, call
import pytest
import pytest_mock
import package_statistic


def test_correct_arch():
    assert package_statistic.parse_arch(["test", "arm64"]) == "arm64"


def test_incorect_arch():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        package_statistic.parse_arch(["test", "dfsd"])
    assert pytest_wrapped_e.value.code == 1


def test_process_content_file():
    expected_result = {"mate-applets-common\n": 2, "mate-user-guide\n": 1}
    with open("content_file_test.txt") as content_file:
        result = package_statistic.process_content_file(content_file)
        assert expected_result == result

@patch('builtins.print')
def test_std_output(mocked_print):
    with open("content_file_test.txt") as content_file:
      result = package_statistic.process_content_file(content_file)
    package_statistic.print_top_10_packages(result)
    assert mocked_print.mock_calls == [call('1. mate-applets-common\n\t2'), call('2. mate-user-guide\n\t1')]

def test_download_file():
    with tempfile.TemporaryDirectory() as tempdir:
        arch = "arm64"
        try:
            file_path = package_statistic.download_file(tempdir, arch)
        except:
            pytest.fail("Could not download the file")

        assert os.path.isfile(file_path)

@patch('builtins.print')
def test_end_to_end(mocked_print):
    sys.argv = ["test", "arm64"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        package_statistic.main()
    assert pytest_wrapped_e.value.code == 0
    assert len(mocked_print.mock_calls) == 10
