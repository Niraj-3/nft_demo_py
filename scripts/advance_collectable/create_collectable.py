

from webbrowser import get

from web3 import Web3
from brownie import AdvancedCollectable
from scripts.helpful_scripts import fund_with_link, get_account

def main():
    account = get_account();
    advanced_collectable = AdvancedCollectable[-1];
    fund_with_link(advanced_collectable.address,amount=Web3.toWei(0.1,"ether"))
    creation_transaction = advanced_collectable.createCollectable({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")