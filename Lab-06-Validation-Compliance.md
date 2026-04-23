# Lab 6: Validation and Compliance

Automation isn't just about *configuring* devices; it's also about *verifying* that the network is actually healthy. This is the foundation of **Intent-Based Networking (IBN)**.

## 🧠 Core Concept: Operational State
- **Configuration:** What you *told* the router to do.
- **Operational State:** What the router is *actually* doing.

In this lab, we check if OSPF has successfully found its neighbors. If it hasn't, your network is broken, even if your configuration is "perfect."

---

## Task: Create the `lab06_validation.yml` Playbook

```yaml
---
- name: Lab 6 - Network Health Validation
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
          - "ospf_neighbors.stdout[0] | regex_search('[0-9]+\\\\.[0-9]+\\\\.[0-9]+\\\\.[0-9]+')"
        fail_msg: "CRITICAL FAILURE: No OSPF neighbors found! Routing is NOT converged."
        success_msg: "SUCCESS: OSPF neighbors verified. The network is alive!"
```

### 🔍 Detailed Logic Breakdown:

1.  **`register: ospf_neighbors`**: This captures the output of the "show" command and saves it in a temporary variable.
2.  **`regex_search`**: This is a **Regular Expression**. We are scanning the text for any string that looks like an IP address (a Neighbor ID). 
3.  **`assert`**: This is your "Automated Auditor." If the test fails, the playbook stops immediately and alerts you.

---

## Part 2: The Isolation Test (Definitive Failure) 🔴

To prove this works, you must see it fail. 

### Task: Manually break the network
Log into your **S1-R1** router via SSH and shut down all peered interfaces:
```bash
conf t
interface Ethernet0/1
  shutdown
interface Ethernet0/2
  shutdown
interface Ethernet0/3
  shutdown
end
```

Wait 30 seconds for OSPF to time out, then run:
```bash
ansible-playbook -i inventory.yml lab06_validation.yml
```

### 🔍 Analyzing the Failure
You should see a **RED** error message. This is exactly what a network engineer wants to see—a clear, automated alert that a specific device is isolated.

### 💡 Industry Pro-Tip: Automated Remediation
In advanced environments, if this validation fails, the system can automatically run **Lab 4** to fix the interfaces without a human ever getting involved!

---

## 📂 Deep Dive: Regular Expressions (Regex)
Regex is a language for searching text. In this lab, we used:
`[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+`

- **`[0-9]`**: Matches any number between 0 and 9.
- **`+`**: Matches "one or more" of the previous item.
- **`\.`**: Matches a literal period (we use the backslash because a normal period matches *anything* in Regex).

**Pro-Tip:** You can test your Regex patterns at [regex101.com](https://regex101.com). It is the #1 tool for network automation engineers!

---

## ❓ Knowledge Check
1.  What does the `register` keyword do?
2.  What is a Regular Expression (Regex) used for in this lab?
3.  Why is it important to verify the "Operational State" after making a change?
