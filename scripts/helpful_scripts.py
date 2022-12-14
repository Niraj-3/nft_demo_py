from web3 import Web3
from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock,Contract


OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development","ganache","mainnet-fork-dev"]

breed_mapping = {1:"PUG",2:"SHIBA_INU", 3:"ST_BERNARD"}
def get_breed(breed_number):
    return breed_mapping[breed_number]

    
def get_account(index=None,id=None):
    if index:
        return accounts[index]
    
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token":LinkToken, "vrf_coordinator":VRFCoordinatorMock}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type)<=0:
            deploy_mocks()
        contract = contract_type[-1];
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
    return contract


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1,"ether")):

    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    sending_txn = link_token.transfer(contract_address,amount,{"from":account})
    sending_txn.wait(1)
    print(f"Funded {contract_address}")
    return sending_txn