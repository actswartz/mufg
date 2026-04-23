# Lab 6: Validation and Compliance

Use the `assert` module to verify that OSPF has formed neighbors.

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
        fail_msg: "No OSPF neighbors found!"
        success_msg: "OSPF neighbors verified."
```
