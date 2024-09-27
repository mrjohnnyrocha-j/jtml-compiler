import unittest
from compiler.intermediate_rep import IntermediateRepresentationGenerator

class TestIntermediateRepresentationGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = IntermediateRepresentationGenerator()

    def test_generate_ir(self):
        ast = "dummy_ast"
        ir = self.generator.generate(ast)
        self.assertIn('Generated IR (PKey-Tes)', ir)

if __name__ == '__main__':
    unittest.main()
