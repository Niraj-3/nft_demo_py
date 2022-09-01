from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENT,get_account,get_contract
from scripts.advance_collectable.deploy_and_create import deploy_and_create
import pytest

def test_can_create_advanced_collectable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    advanced_collectable,creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    randomNumber=777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId,randomNumber,advanced_collectable.address,{"from":get_account()}
    )

    assert advanced_collectable.tokenCounter() == 1
    assert advanced_collectable.tokenIdToBreed(0) == randomNumber%3