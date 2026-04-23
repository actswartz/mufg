# Lab 9: Exception Handling

In the real world, things go wrong. A router might be offline, a command might be misspelled, or a network link might fail. **Exception Handling** allows your playbook to "fail gracefully" instead of just crashing.

## 🧠 Core Concept: Block, Rescue, Always
- **`block`**: The tasks you *want* to run.
- **`rescue`**: The tasks that run *only if* something in the block fails. (Like "Error Handling").
- **`always`**: Tasks that run no matter what happens (success or failure).

## Task: Create the `lab09_exceptions.yml` Playbook

```yaml
---
- name: Lab 9 - Resilience Test
  hosts: routers
  gather_facts: false
  tasks:
    - block:
        - name: Attempt to run an invalid command (This will fail)
          cisco.ios.ios_command:
            commands: "show flux-capacitor status"
            
      rescue:
        - name: Handle the error
          debug:
            msg: "Caught the error! The flux-capacitor is missing, but the playbook continues."

      always:
        - name: Final Cleanup
          debug:
            msg: "This message appears even if the command failed. Perfect for closing log files."
```

### 🔍 Why is this useful?
Imagine you are updating 100 routers. If router #5 is offline, normally Ansible stops the whole play. With a `rescue` block, you can tell Ansible: "If you can't reach the router, log the error and move on to router #6."

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab09_exceptions.yml
```

**Observation:** Notice that even though the "invalid command" task failed, the playbook overall reports **SUCCESS** because the error was "rescued".
