import pytest
from baseline.essay.file import File


class TestFile:
    def test_file_read_correct(self, file_path_correct):
        file = File(file_path_correct)
        x = file.read()
        assert (x == "test")

    # def test_file_read_incorrect(self, file_path_incorrect):
    #     with

    def test_file_write(self, file_path_correct):
        file = File(file_path_correct)
        x = file.write('qwe')
        y = file.read()
        assert (y == 'qwe')
