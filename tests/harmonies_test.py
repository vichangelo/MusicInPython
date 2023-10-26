import musicinpython.harmonies as harmonies


def test_get_scale_harmony():
    harm = harmonies.get_scale_harmony("B Lydian")
    assert "Fm7(b5)" in harm
