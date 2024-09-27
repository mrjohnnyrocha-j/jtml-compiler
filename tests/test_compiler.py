import unittest
from compiler.compiler import JTMLCompiler

class TestJTMLCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = JTMLCompiler()

    def test_compile(self):
        result = self.compiler.compile('example.jtml', pqtt_enabled=True)
        self.assertIn('Compiled example.jtml with PQTT=True', result)

    def test_progressive_compile(self):
        result = self.compiler.progressive_compile('example.jtml', stage='intermediate')
        self.assertIn('Intermediate Representation', result)

if __name__ == '__main__':
    unittest.main()
