from pathlib import Path

from appdata import get_home_folder, prepare_ext


class TestUtils:
    def test_home_path(self):
        assert get_home_folder() == Path.home()

    def test_ext_preparation_1(self):
        assert prepare_ext('.ext') == '.ext'

    def test_ext_preparation_2(self):
        assert prepare_ext('ext') == '.ext'

    def test_ext_preparation_3(self):
        assert prepare_ext('') == ''

    def test_ext_preparation_4(self):
        assert prepare_ext('.') == ''

    def test_ext_preparation_5(self):
        assert prepare_ext('..') == ''

    def test_ext_preparation_6(self):
        assert prepare_ext('...') == ''

    def test_ext_preparation_7(self):
        assert prepare_ext(None) == ''
