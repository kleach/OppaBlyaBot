from oppablyabot.util.paths.paths import PROJECT
import unittest


class PathsTestCase(unittest.TestCase):
    def test_project_path(self):
        print(PROJECT)
        assert PROJECT == 'a'
