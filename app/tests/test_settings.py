import pytest
import sys
sys.path.append("/home/dsteffen/python/wiki/app")

from settings import Settings

rs = Settings()
bla = rs.readConfig();

def test_readConfig():
    assert rs.readConfig() == 'kekse'