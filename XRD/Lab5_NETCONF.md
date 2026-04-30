# Lab 5: Programmatic Interface (NETCONF & YANG)

## Lab Overview
In this lab, you will transition from being a "CLI Engineer" to an "Automation Architect." You will enable the programmatic interface of IOS-XR, allowing external computers to talk to the router using structured data.

By the end of this lab, you will have:
1. Enabled the **NETCONF-YANG** agent on the router.
2. Verified that the router is listening for programmatic requests.
3. Learned the difference between **Unstructured Data** (CLI) and **Structured Data** (YANG).

---

## Part 1: Enabling the NETCONF Agent 

### What is happening?
By default, the router only listens for humans (SSH CLI). We are going to enable the `netconf-yang agent`, which allows the router to accept XML-formatted messages over SSH.

### The Purpose
APIs (Application Programming Interfaces) are the foundation of modern networking. Tools like Ansible, Terraform, and Python use NETCONF to automate changes safely and at scale.

### ️ Step-by-Step:
Enable the programmatic agent on **both routers**:
```ios
conf t
 netconf-yang agent
 ssh
 !
 commit
```

---

## Part 2: Verification of the Agent 

### What is happening?
XRd runs NETCONF as a separate process. We need to verify that the process started and is healthy.

### ️ Step-by-Step:

#### Command: `show processes netconf`
Check if the process is in the `Run` state.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show processes netconf
         Job Id: 1145
           PID: 4521
     Executable path: /pkg/bin/netconf
       Args: -p 830
          State: Run
```

#### Command: `show netconf-yang statistics`
This shows you how many automated requests the router has handled.

---

## Part 3: The Hello Handshake (Testing the API) 

### ️ Step-by-Step:
From the **Lab Server CLI** (not inside the router), try to perform a NETCONF handshake. This "tricks" the router into sending you its list of capabilities (YANG models).

```bash
# Replace 310XX with your XR1 port
ssh -4 -p 310XX clab@136.243.78.83 -s netconf
```
> **Note:** The `-s netconf` flag tells SSH to use the **NETCONF Subsystem** instead of the Shell. You will see a massive wall of XML text—this is the router saying "Hello! I support these 500 different data models."

---

## Part 4: What is a YANG Model? 

### Concept
Think of a **YANG Model** as a "Spreadsheet Template." 
- The **CLI** is like a handwritten note: "Put the IP 1.1.1.1 on Gi0/0/0/0."
- The **YANG Model** is a strict form:
 - Column A: Interface Name
 - Column B: IPv4 Address
 - Column C: Status
 
This structure ensures that an automation script always knows exactly where to find the data it needs.

---

## Summary Checklist
- [ ] Enabled the `netconf-yang agent`.
- [ ] Verified the `netconf` process is running.
- [ ] Successfully performed a NETCONF "Hello" via the SSH subsystem.
