import requests
import json
import re

# AWX Configuration
BASE_URL = "http://localhost:30854/api/v2"
AUTH = ("admin2", "800-ePlus")

# Standard Inventory Variables
INVENTORY_VARS = """---
ansible_user: admin
ansible_password: 800-ePlus
ansible_ssh_pass: 800-ePlus
ansible_become_pass: 800-ePlus
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: cisco.ios.ios
ansible_become: true
ansible_become_method: enable
ansible_ssh_extra_args: "-o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no"
ansible_network_cli_ssh_type: libssh
"""

def get_all_orgs():
    r = requests.get(f"{BASE_URL}/organizations/?page_size=100", auth=AUTH)
    return r.json()['results']

def get_inventory_for_org(org_id):
    r = requests.get(f"{BASE_URL}/inventories/?organization={org_id}", auth=AUTH)
    results = r.json()['results']
    return results[0] if results else None

def update_inventory_vars(inv_id, inv_name):
    print(f"Updating Variables for Inventory: {inv_name} (ID: {inv_id})")
    r = requests.patch(f"{BASE_URL}/inventories/{inv_id}/", auth=AUTH, json={"variables": INVENTORY_VARS})
    if r.status_code == 200:
        print(f"  Successfully updated {inv_name}")
    else:
        print(f"  Error updating {inv_name}: {r.text}")

def ensure_machine_credential(org_id, org_name):
    cred_name = "Cisco Router Login"
    # Check if exists
    r = requests.get(f"{BASE_URL}/credentials/?name={cred_name}&organization={org_id}", auth=AUTH)
    if r.json()['results']:
        print(f"  Credential '{cred_name}' already exists in {org_name}.")
        return

    print(f"  Creating Credential: {cred_name} in {org_name}")
    data = {
        "name": cred_name,
        "organization": org_id,
        "credential_type": 1, # Machine
        "inputs": {
            "username": "admin",
            "password": "800-ePlus",
            "become_method": "enable",
            "become_password": "800-ePlus"
        }
    }
    r = requests.post(f"{BASE_URL}/credentials/", auth=AUTH, json=data)
    if r.status_code != 201:
        print(f"  Error creating credential in {org_name}: {r.text}")

# Main Execution
orgs = get_all_orgs()
for org in orgs:
    # Filter for student Orgs (S1 to S15)
    if re.search(r'S\d+', org['name']):
        print(f"Processing Organization: {org['name']} (ID: {org['id']})")
        
        # 1. Update Inventory Variables
        inv = get_inventory_for_org(org['id'])
        if inv:
            update_inventory_vars(inv['id'], inv['name'])
        else:
            print(f"  No inventory found for {org['name']}")
            
        # 2. Ensure Machine Credential
        ensure_machine_credential(org['id'], org['name'])
        print("-" * 30)

print("Bulk Update Finished.")
