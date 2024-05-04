from preprod import commons

def test_run_and_check():
    assert commons.run_and_check("pwd")
    assert not commons.run_and_check("pwd", expected_returncode=1)
    
