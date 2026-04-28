import requests
import json
import urllib3
import re

# Disable insecure request warnings for local lab environment
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# AWX Configuration
BASE_URL = "http://localhost:30854/api/v2"
AUTH = ("admin2", "800-ePlus")
REPO_URL = "https://github.com/actswartz/mufg"

def get_resource(endpoint):
    r = requests.get(f"{BASE_URL}/{endpoint}/", auth=AUTH, verify=False)
    if r.status_code == 200:
        return r.json()['results']
    return []

def find_or_create(endpoint, name, data):
    # Check if exists
    r = requests.get(f"{BASE_URL}/{endpoint}/?name={name}", auth=AUTH, verify=False)
    results = r.json().get('results', [])
    if results:
        print(f"  {endpoint.capitalize()} '{name}' already exists.")
        return results[0]['id']
    
    print(f"  Creating {endpoint}: {name}")
    r = requests.post(f"{BASE_URL}/{endpoint}/", auth=AUTH, json=data, verify=False)
    if r.status_code in [201, 200]:
        return r.json()['id']
    else:
        print(f"  Error creating {endpoint} {name}: {r.text}")
        return None

def main():
    for i in range(1, 16):
        s_name = f"S{i:02d}"
        org_name = f"{s_name}- Org-{s_name}"
        
        print(f"Processing {s_name}...")
        
        # 1. Organization
        org_id = find_or_create("organizations", org_name, {"name": org_name})
        if not org_id: continue

        # 2. Credential
        cred_name = f"{s_name}- Cisco Router Login"
        cred_data = {
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
        cred_id = find_or_create("credentials", cred_name, cred_data)

        # 3. Project
        proj_name = f"{s_name}- AAP Workshop Code"
        proj_data = {
            "name": proj_name,
            "organization": org_id,
            "scm_type": "git",
            "scm_url": REPO_URL,
            "scm_update_on_launch": True
        }
        proj_id = find_or_create("projects", proj_name, proj_data)
        
        # Trigger Project Sync
        if proj_id:
            requests.post(f"{BASE_URL}/projects/{proj_id}/update/", auth=AUTH, verify=False)

        # 4. Inventory
        inv_name = f"{s_name}- Student Pod Inventory"
        inv_data = {
            "name": inv_name,
            "organization": org_id
        }
        inv_id = find_or_create("inventories", inv_name, inv_data)

        # 5. Job Template
        jt_name = f"{s_name}- 01 - Gather Cisco Facts"
        jt_data = {
            "name": jt_name,
            "project": proj_id,
            "inventory": inv_id,
            "playbook": "lab01_facts.yml",
            "job_type": "run"
        }
        jt_id = find_or_create("job_templates", jt_name, jt_data)
        
        # Associate Credential with Template
        if jt_id and cred_id:
            requests.post(f"{BASE_URL}/job_templates/{jt_id}/credentials/", 
                         auth=AUTH, json={"id": cred_id}, verify=False)

    print("AWX Standardization Finished.")

if __name__ == "__main__":
    main()
