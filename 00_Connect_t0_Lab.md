<img src="images/3r.jpg" width="400" alt="Network Topology">

**🚀 Mission Prompt:** Establish your bridgehead. Your goal is to successfully connect to the Lab Server and verify you can reach your Pod's management network.

---

### 🛠️ How to Connect to a Router
If you need to verify your work or troubleshoot manually, follow these steps:
1.  **Requirement:** You must be logged into the Lab Server.
2.  **Connect via SSH (Replace X with your Pod Number):**
    *   `ssh admin@S<X>-R1`
    *   `ssh admin@S<X>-R2`
    *   `ssh admin@S<X>-R3`
3.  **Password:** `800-ePlus`
4.  **Useful Verification Commands:**
    *   `sh ip int brief`
    *   `sh run`

---

# Lab 0: Classroom Connection Instructions

Welcome to the lab environment! 👋 Follow the steps below to connect to your assigned Student User and verify your environment.

## 🧠 Core Concept: The Jump Server
In modern networking, critical infrastructure is rarely exposed directly to the internet. We use a **Jump Server** (or "Bastion Host") as a secure single point of entry. You will log into this Ubuntu server using your assigned **Student Account** (`S1`, `S2`, etc.).

---

## Part 1: Connect to the Lab Server

From your terminal or SSH client (Mac Terminal, Windows PowerShell, or PuTTY), run the following command.

```bash
# Replace XX with your assigned number (e.g., S5)
ssh S<XX>@LAB_SERVER_IP
```

**Password:**
```text
800-ePlus
```

---

## Part 2: Your Lab Identity

Each student has a unique identity and pod assignment:
- **Username:** `S1` through `S15`
- **Password:** `800-ePlus`
- **Router Prefix:** Your routers start with your username (e.g., `S5-R1`).

### 🔍 Verification Task
Once you are logged into the Ubuntu server, verify you can "see" your routers by pinging them by name:
```bash
ping -c 3 S<XX>-R1
```
*(If the ping fails, notify your instructor immediately.)*

---

## Part 3: Environment Setup 🏗️

All the workshop materials are pre-cloned for you. 

1. Navigate to the workshop directory:
   ```bash
   cd ~/dlr
   ```
2. List the files to ensure you see the lab modules:
   ```bash
   ls -l
   ```

---

## 📂 Deep Dive: SSH Keys vs Passwords
In this lab, we use passwords for simplicity. However, in professional environments, we use **SSH Keys** (Public/Private key pairs).
- **Public Key:** Stored on the router.
- **Private Key:** Stored only on your machine.
This is significantly more secure and allows you to log in without typing a password every time.

---

## ❓ Knowledge Check
1. What is the name of your assigned student user account?
2. What is the command used to log into the Lab Server?
3. Why do we use a Jump Server in a professional network?

---

## 📺 Video Tutorial: Watch & Learn
For a visual walkthrough of the connection process, check out this tutorial:
[https://www.youtube.com/watch?v=346pNooH_N0](https://www.youtube.com/watch?v=346pNooH_N0)
