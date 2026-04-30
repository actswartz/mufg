# Lab 2: Modern IGP (IS-IS)

## Lab Overview
In this lab, you will move from static connections to dynamic routing. You will configure **IS-IS (Intermediate System to Intermediate System)** between your pod routers. 

By the end of this lab, you will have:
1. Created **Loopback** interfaces (the "Identity" of a router).
2. Configured **ISO/NET** addresses (the unique requirement of IS-IS).
3. Established an IS-IS adjacency between `xr1` and `xr2`.
4. Verified the exchange of routing information via the **Link State Database**.

---

## Part 1: Loopbacks & The ISO Network Entity Title (NET) 

### What is happening?
IS-IS does not run on top of IP; it runs directly on the Data Link Layer (L2). Because of this, it doesn't use IP addresses to identify routers. Instead, it uses an **ISO NET address**.

### The Purpose
By running independently of IP, IS-IS can route for both IPv4 and IPv6 simultaneously without needing two separate protocols.

### ️ Step-by-Step:
Configure a Loopback and the NET address on **Router 1**:
```ios
conf t
 interface Loopback0
 ipv4 address 1.1.1.X 255.255.255.255 !! Use 1.1.1.1 for Pod 1, 1.1.1.2 for Pod 2, etc.
 !
 router isis POD_CORE
 net 49.0001.0000.0000.000X.00    !! Use X as your Pod number
 address-family ipv4 unicast
 !
 commit
```

**Note on NET address format:** `49.0001.0000.0000.0001.00`
- `49.0001`: The Area ID.
- `0000.0000.0001`: The System ID (Must be unique for every router).
- `00`: The selector (Always 00 for routers).

---

## Part 2: Enabling the Protocol on Interfaces 

### What is happening?
Unlike OSPF where you often use a `network` command, in IS-IS, you typically enable the protocol directly under the specific interfaces you want to participate in routing.

### ️ Step-by-Step:
Enable IS-IS on the P2P and Loopback interfaces (**Router 1**):
```ios
conf t
 interface Loopback0
 address-family ipv4 unicast
  isis POD_CORE
 !
 interface GigabitEthernet0/0/0/0
 address-family ipv4 unicast
  isis POD_CORE
 !
 commit
```

*Repeat these steps on **Router 2**, using `2.2.2.X` for the loopback and a different System ID (e.g., `...000X.0002.00`).*

---

## Part 3: Verification 

#### Command: `show isis adjacency`
This is your primary check. It confirms that the two routers have successfully "shaken hands" and are now neighbors.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show isis adjacency
IS-IS POD_CORE Level-1-2 adjacencies:
System Id   Interface        SNPA      State Hold Changed Type IETF-BFD
p1-xr2     Gi0/0/0/0        *PtoP*     Up   27  00:05:12 L1L2 None
```

#### Command: `show route isis`
Check the routing table to see if you have learned the Loopback address of the other router.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show route isis
i L2 2.2.2.1/32 [115/20] via 10.1.1.2, 00:04:45, GigabitEthernet0/0/0/0
```

---

## Summary Checklist
- [ ] Configured unique NET addresses for both routers.
- [ ] Enabled IS-IS on Loopbacks and P2P links.
- [ ] Verified the Adjacency state is `Up`.
- [ ] Successfully saw the neighbor's loopback in the routing table.
