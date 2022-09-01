
from pathlib import Path
from brownie import AdvancedCollectable,network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advanced_collectable = AdvancedCollectable[-1]
    number_of_advanced_collectable = advanced_collectable.tokenCounter()
    print(f"You have {number_of_advanced_collectable} collectable")
    for tokenId in range(number_of_advanced_collectable):
        breed = get_breed(advanced_collectable.tokenIdToBreed(tokenId))
        metadata_file_name = f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        collectable_template = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating MetaData file : {metadata_file_name}")
            collectable_template["name"] = breed
            collectable_template["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_","-")+".png"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectable_template["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectable_template, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
