# Lab 6: Validation and Compliance

Automation isn't just about *configuring* devices; it's also about *verifying* that the network is actually healthy. This is known as **Intent-Based Networking**.

## 🧠 Core Concept: Operational State
- **Configuration:** What we *want* to happen (e.g., "Interface Ethernet0/1 should be 12.12.12.1").
- **Operational State:** What is *actually* happening (e.g., "Is the interface up? Can I see my neighbor?").

In this lab, we use Ansible to "scrape" the output of a Cisco command and test it against our requirements.

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

    - name: Display Raw Output for Learning
      debug:
        var: ospf_neighbors.stdout[0]

    - name: Assert OSPF has Neighbors
      assert:
        that:
          - "ospf_neighbors.stdout[0] | regex_search('[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+')"
        fail_msg: "CRITICAL: No OSPF neighbors found! Routing is NOT converged."
        success_msg: "SUCCESS: OSPF neighbors verified. The network is alive!"
```

### 🔍 Detailed Logic Breakdown:

1.  **`register: ospf_neighbors`**: 
    - Normally, Ansible runs a command and just shows you the result on the screen. 
    - `register` tells Ansible: "Take the entire output of this command and save it into a variable named `ospf_neighbors` so I can use it later."

2.  **`ospf_neighbors.stdout[0]`**:
    - The registered variable is a complex object. `stdout` is the list of results (one for each command run). 
    - `[0]` means "the output of the first command in the list."

3.  **`regex_search` (Regular Expressions)**:
    - OSPF neighbor output can be messy. It contains headers, timers, and interface names.
    - We use a **Regex Pattern** `[0-9]+\.[0-9]+...` to look for something that looks like an IP address.
    - If a neighbor exists, their "Neighbor ID" (an IP) will be in the output. If no neighbor exists, the output will be empty or just headers, and the regex will fail.

4.  **`assert`**:
    - This is the "Judge." If the condition in `that:` is true, the play continues. If it's false, the playbook **fails loudly**, which is exactly what you want in a production environment if the network is down.

## Part 2: Running the Validation 🛠️

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab06_validation.yml
```

### 🧪 Experiment: See it fail!
If you want to see the error message, go to one of your routers and shut down an interface:
```bash
conf t
int e0/1
shut
```
Now run the validation playbook again. You should see a **RED** failure message with your custom `fail_msg`.
