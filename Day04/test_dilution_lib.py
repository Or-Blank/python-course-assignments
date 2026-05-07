import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
#Before looking anywhere else, look in the same folder as this file when importing modules, Make sure Python can import dilution_lib from this folder, even if there is another module with the same name elsewhere in the Python path.
import dilution_lib

#Creates a test class using Python’s built‑in testing framework
class TestDilutionLib(unittest.TestCase):
    def test_calculation_of_c1(self):
        result = dilution_lib.Calculation_of_C1(C2=2.0, V2=50.0, V1=10.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculation_of_v1(self):
        result = dilution_lib.Calculation_of_V1(C1=5.0, C2=2.0, V2=50.0)
        self.assertAlmostEqual(result, 20.0)

    def test_calculation_of_c2(self):
        result = dilution_lib.Calculation_of_C2(C1=10.0, V1=5.0, V2=25.0)
        self.assertAlmostEqual(result, 2.0)

    def test_calculation_of_v2(self):
        result = dilution_lib.Calculation_of_V2(C1=8.0, V1=5.0, C2=2.0)
        self.assertAlmostEqual(result, 20.0)

    def test_calculation_of_c1_zero_v1_returns_none(self):
        result = dilution_lib.Calculation_of_C1(C2=2.0, V2=50.0, V1=0.0)
        self.assertIsNone(result)

    def test_calculation_of_v1_zero_c1_returns_none(self):
        result = dilution_lib.Calculation_of_V1(C1=0.0, C2=2.0, V2=50.0)
        self.assertIsNone(result)

    def test_calculation_of_c2_zero_v2_returns_none(self):
        result = dilution_lib.Calculation_of_C2(C1=10.0, V1=5.0, V2=0.0)
        self.assertIsNone(result)

    def test_calculation_of_v2_zero_c2_returns_none(self):
        result = dilution_lib.Calculation_of_V2(C1=8.0, V1=5.0, C2=0.0)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
