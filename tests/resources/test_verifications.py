import pytest

from mati import Client


@pytest.mark.vcr
def test_retrieve_full_verification(client: Client):
    verification = client.verifications.retrieve('5d9fb1f5bfbfac001a349bfb')
    assert verification.documents
    assert verification.identity['status'] == 'verified'
    govt = verification.govt_id_document
    assert govt.country == 'MX'
    assert govt.document_type == 'dni'
    assert govt.address == 'Varsovia 36, 06600 CDMX'
    assert govt.full_name == 'FIRST LAST'
    govt.fields = {}
    assert not govt.address
    assert not govt.full_name
    assert verification.govt_id_validation.is_valid
    assert verification.proof_of_life_validation.is_valid
    assert verification.proof_of_residency_validation.is_valid
    assert (
        verification.proof_of_residency_document.address
        == 'Varsovia 36, 06600 CDMX'
    )
    verification.documents = []
    assert not verification.govt_id_validation


@pytest.mark.vcr
def test_verification_without_liveness(client: Client):
    verification = client.verifications.retrieve('5d9fb1f5bfbfac001a349bfb')
    verification.steps = []
    assert not verification.proof_of_life_document


@pytest.mark.vcr
def test_verification_without_poa(client: Client):
    verification = client.verifications.retrieve('5d9fb1f5bfbfac001a349bfb')
    verification.documents = [verification.documents[0]]
    assert not verification.proof_of_residency_document
    assert not verification.proof_of_residency_validation


@pytest.mark.vcr
def test_verification_without_pol(client: Client):
    verification = client.verifications.retrieve('621faa3869ef6d001cf439c7')
    verification.steps = None
    assert not verification.proof_of_life_validation


@pytest.mark.vcr
def test_verification_is_pending(client: Client):
    verification = client.verifications.retrieve('61c4181a668ff5001c017ff5')
    verification.identity['status'] = 'running'
    assert verification.is_pending
