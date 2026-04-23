# Lab 6: Validation and Compliance

Automation isn't just about *configuring* devices; it's also about *verifying* that they are working correctly.

## 🧠 Core Concept: Operational State
Configuration is what we *tell* the router to do. State is what the router is *actually doing*. 
In this lab, we check if OSPF has successfully found its neighbors.

## Task: Create the `lab06_validation.yml` Playbook

```yaml
---
- name: Lab 6 - Validation
  hosts: routers
  gather_facts: false
  tasks:
    - name: Check OSPF Neighbors
      cisco.ios.ios_command:
        commands: "show ip ospf neighbor"
      register: ospf_neighbors

    - name: Assert OSPF has Neighbors
      assert:
        that:
          - "ospf_neighbors.stdout[0] | regex_search('[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+')"
        fail_msg: "No OSPF neighbors found! Routing might be broken."
        success_msg: "OSPF neighbors verified. The network is alive!"
```

### 🔍 Breakdown of Validation Logic:
1.  **`cisco.ios.ios_command`**: Runs a standard "show" command.
2.  **`register: ospf_neighbors`**: Saves the output of that command into a temporary variable called `ospf_neighbors`.
3.  **`assert`**: This is a test module.
    *   **`that:`**: The condition to check. Here, we use a **Regular Expression** (`regex_search`) to look for an IP address in the output.
    *   If an IP address (a neighbor ID) is found, the test passes. If the output is empty, the playbook stops and shows an error.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab06_validation.yml
```
