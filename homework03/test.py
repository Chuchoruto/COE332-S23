from water_examination import calc_turbidity, safe_Time
import pytest

def test_calc_turbidity():
    assert calc_turbidity(0.987, 1.12) == pytest.approx(1.10544)

def test_safe_Time():
    assert safe_Time(1.14) == pytest.approx(6.485678)

