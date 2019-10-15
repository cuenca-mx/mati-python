import pytest

from mati import Client


@pytest.mark.vcr
def test_retrieve_verification(client: Client):
    verification = client.verifications.retrieve('5d9fb1f5bfbfac001a349bfb')
    assert verification
