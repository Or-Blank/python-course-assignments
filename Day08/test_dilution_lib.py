"""Minimal tests for dilution_lib business logic"""
import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "Day04"))

from dilution_lib import (
    Calculation_of_C1,
    Calculation_of_V1,
    Calculation_of_C2,
    Calculation_of_V2,
)


class TestCalculationOfC1:
    def test_basic_calculation(self):
        assert Calculation_of_C1(C2=2.0, V2=100, V1=50) == 4.0

    def test_zero_v1_returns_none(self):
        assert Calculation_of_C1(C2=2.0, V2=100, V1=0) is None


class TestCalculationOfV1:
    def test_basic_calculation(self):
        assert Calculation_of_V1(C1=4.0, C2=2.0, V2=100) == 50.0

    def test_zero_c1_returns_none(self):
        assert Calculation_of_V1(C1=0, C2=2.0, V2=100) is None


class TestCalculationOfC2:
    def test_basic_calculation(self):
        assert Calculation_of_C2(C1=4.0, V1=50, V2=100) == 2.0

    def test_zero_v2_returns_none(self):
        assert Calculation_of_C2(C1=4.0, V1=50, V2=0) is None


class TestCalculationOfV2:
    def test_basic_calculation(self):
        assert Calculation_of_V2(C1=4.0, V1=50, C2=2.0) == 100.0

    def test_zero_c2_returns_none(self):
        assert Calculation_of_V2(C1=4.0, V1=50, C2=0) is None

