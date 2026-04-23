# Lab 9: Exception Handling

Learn how to use `block`, `rescue`, and `always` to make your playbooks resilient.

## Task: Create the `lab09_exceptions.yml` Playbook

```yaml
---
- name: Lab 9 - Exception Handling
  hosts: routers
  gather_facts: false
  tasks:
    - block:
        - name: Attempt to run invalid command
          cisco.ios.ios_command:
            commands: "show invalid command"
      rescue:
        - name: Handle Error
          debug:
            msg: "Captured an error as expected for Lab 9!"
      always:
        - name: Always Run
          debug:
            msg: "This task always runs."
```
