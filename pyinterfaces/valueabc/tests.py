import os
import unittest

from existing_directory import ExistingDirectory
from existing_file import ExistingFile

class InterfaceTests(unittest.TestCase):
    def test_existingdirectory(self):
        self.assert_(isinstance('test_bypath', ExistingDirectory))
        self.assert_(not isinstance('_test_bypath', ExistingDirectory))

        self.assert_(os.path.exists('__init__.py'))
        self.assert_(not isinstance('__init__.py', ExistingDirectory))

    def test_existingfile(self):


        self.assert_(isinstance('__init__.py', ExistingFile))
        self.assert_(ExistingFile('__init__.py') == '__init__.py')
        self.assertRaises(TypeError, lambda: ExistingFile(12))
        self.assertRaises(IOError, lambda: ExistingFile('wargarbl'))

if __name__ == "__main__":
    unittest.main()
