# Lab 1: Cisco XRd Foundations & The Two-Stage Configuration Model

## 📖 Lab Overview
Welcome to your first lab with **Cisco XRd** (IOS-XR in a container). In this lab, you will move beyond the traditional "classic" IOS (like IOS-XE) and learn the specialized architecture of a Service Provider operating system. 

By the end of this lab, you will have:
1.  Navigated the unique XR prompt and hardware nomenclature.
2.  Mastered the **Two-Stage Configuration Model** (Candidate vs. Running).
3.  Established a functional **Point-to-Point (P2P)** data-plane link between your two pod routers.
4.  Used built-in troubleshooting tools to verify connectivity.

---

## Part 1: Navigating the XR Architecture 🧭

### 📖 What is happening?
Unlike traditional routers, IOS-XR is built on a Linux microservices architecture. When you connect, you aren't just "on a router"; you are interacting with a specialized process running on top of a 64-bit Linux kernel.

### 🎯 The Purpose
XR was designed for "99.999% availability." By separating the operating system into distinct processes, a failure in the BGP process won't crash the entire router.

### 🛠️ Step-by-Step:
Log into your first router using the command provided in your access guide:
```bash
ssh -4 -p 31011 clab@136.243.78.83
```

#### 🔍 Command: `show version`
This command identifies the software version, the uptime, and the specific "label" of the build.

**Sample Output:**
```text
RP/0/RP0/CPU0:xr1# show version
Cisco IOS XR Software, Version 24.1.1
Copyright (c) 2013-2024 by Cisco Systems, Inc.

Build Information:
 Built By     : de-build-9
 Built On     : Wed Feb 21 00:30:12 PST 2024
 Built Host   : iox-docker-037

IOS XR 64 bit x86 Full Software
```

#### 🔍 The Prompt: `RP/0/RP0/CPU0:xr1#`
XR uses a "Location-based" prompt. 
- **RP:** Route Processor.
- **0:** Rack number.
- **RP0:** Slot number.
- **CPU0:** The specific core/CPU handling this session.
> **Note:** In a massive chassis with 20 line-cards, this nomenclature tells you exactly where you are in the hardware hierarchy.

---

## Part 2: The Two-Stage Configuration Model 🏗️

### 📖 What is happening?
In "Classic" IOS, when you type `hostname MYROUTER`, the change happens instantly. In IOS-XR, you work in a **Candidate Configuration** buffer. Nothing changes until you explicitly "Commit" the code.

### 🎯 The Purpose
This prevents "Fat Finger" mistakes. You can type 50 lines of complex BGP code, review it for errors, and then apply it all at once as a single atomic transaction.

### 🛠️ Step-by-Step:
Enter configuration mode:
```ios
conf t
```

#### 🔍 Command: `hostname p1-xr1`
Change the name of the router. 
> **Note:** Notice that the prompt **did not change** yet! The router is still called `xr1` because the change is only in the "Candidate" buffer.

#### 🔍 Command: `show configuration merge`
This shows you what is currently in your buffer that has *not* yet been applied.

**Sample Output:**
```text
RP/0/RP0/CPU0:xr1(config)# show configuration merge
!! IOS XR Configuration 24.1.1
hostname p1-xr1
end
```

#### 🔍 Command: `commit`
This "pushes" the buffer into the running configuration.
> **Note:** Only after this command will your prompt update to `p1-xr1`.

---

## Part 3: Configuring the Data Plane (P2P Link) 🔗

### 📖 What is happening?
We are going to configure the `Gi0/0/0/0` interface. In our Containerlab topology, this physical "wire" connects directly to the other router in your pod.

### 🎯 The Purpose
In a Service Provider network, we typically use `/31` or `/30` subnets for Point-to-Point links to conserve IP space. This link will be the "bridge" that allows our routers to eventually share routing protocols.

### 🛠️ Step-by-Step:
Configure the IP on **Router 1**:
```ios
conf t
 interface GigabitEthernet0/0/0/0
  description P2P_LINK_TO_XR2
  ipv4 address 10.1.1.1 255.255.255.252
  no shutdown
 commit
```

Configure the IP on **Router 2** (Connect via port `31012`):
```ios
conf t
 interface GigabitEthernet0/0/0/0
  description P2P_LINK_TO_XR1
  ipv4 address 10.1.1.2 255.255.255.252
  no shutdown
 commit
```

---

## Part 4: Verification & Connectivity 🔬

### 📖 What is happening?
We will use operational commands to verify the state of the hardware and the software's ability to "see" its neighbor.

### 🛠️ Step-by-Step:

#### 🔍 Command: `show ipv4 interface brief`
Verify that the interface is `Up` and `Up`. 

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show ipv4 interface brief
Interface                      IP-Address      Status          Protocol Vrf-Name
MgmtEth0/RP0/CPU0/0            172.30.30.11    Up              Up       default
GigabitEthernet0/0/0/0         10.1.1.1        Up              Up       default
```

#### 🔍 Command: `ping 10.1.1.2`
Attempt to reach the other side.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# ping 10.1.1.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.1.1.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms
```

---

## 🏁 Summary Checklist
- [ ] Logged into both XRd nodes.
- [ ] Changed hostnames using the `commit` model.
- [ ] Configured P2P IPs on `Gi0/0/0/0`.
- [ ] Successfully pinged from `p1-xr1` to `p1-xr2`.
