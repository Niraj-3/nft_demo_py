from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENT,get_account
from scripts.simple_collectable.deploy_and_create import deploy_and_create
import pytest

def test_can_create_simple_collectable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    simple_collectable = deploy_and_create()
    assert simple_collectable.ownerOf(0) == get_account()