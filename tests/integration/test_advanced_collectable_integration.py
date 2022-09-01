from brownie import network, AdvancedCollectable
import time
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from scripts.advance_collectable.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectable, creation_transaction = deploy_and_create()
    time.sleep(60)
    # Assert
    assert advanced_collectable.tokenCounter() == 1