# Lab 4: Segment Routing (SR-MPLS Foundations)

## Lab Overview
In this lab, you will explore the modern way of handling MPLS. You will replace traditional label protocols (like LDP) with **Segment Routing (SR)**. 

By the end of this lab, you will have:
1. Enabled **Segment Routing** globally.
2. Assigned a **Prefix-SID** (Segment Identifier) to your Loopback.
3. Integrated SR into the IS-IS process.
4. Verified the label stack in the MPLS forwarding table.

---

## Part 1: Enabling Segment Routing Globally 

### What is happening?
Segment Routing (SR) allows the IGP (IS-IS) to distribute MPLS labels itself. This means we no longer need a separate protocol like LDP or RSVP-TE.

### The Purpose
SR simplifies the network core by reducing the number of protocols you have to manage. It also enables "Traffic Engineering" (steering traffic) using the source routing concept.

### ️ Step-by-Step:
Enable Segment Routing on **both routers**:
```ios
conf t
 segment-routing
 global-block 16000 23999
 !
 commit
```
> **Note:** The **Global Block (SRGB)** is the range of labels reserved for SR. `16000-23999` is the Cisco standard default.

---

## Part 2: Integration with IS-IS 

### What is happening?
We need to tell IS-IS to start carrying label information and assign a specific label (SID) to our Loopback interface.

### ️ Step-by-Step:
Configure **Router 1**:
```ios
conf t
 router isis POD_CORE
 address-family ipv4 unicast
  segment-routing mpls
 !
 interface Loopback0
  address-family ipv4 unicast
  prefix-sid index 11   !! Use 1X where X is your pod number (e.g., Pod 1 = 11)
  !
 commit
```

*Configure **Router 2**, using a different index (e.g., `prefix-sid index 12`).*

---

## Part 3: Verification 

#### Command: `show mpls forwarding`
This shows the actual labels being used to move packets.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show mpls forwarding
Local Outgoing  Prefix       Outgoing   Next Hop    Bytes    
Label Label    or ID       Interface          Switched  
------ ----------- ------------------ ------------ --------------- ----------- 
16012 Pop     2.2.2.1/32     Gi0/0/0/0  10.1.1.2    0      
```
> **Note:** The label `16012` is derived from: SRGB Start (16000) + Index (12) = 16012. This is the "Magic" of SR—labels are predictable!

#### Command: `show isis segment-routing label-table`
Verify that IS-IS is correctly managing the SR labels.

---

## Summary Checklist
- [ ] Enabled the `segment-routing` global process.
- [ ] Enabled `segment-routing mpls` under IS-IS.
- [ ] Assigned a unique `prefix-sid index` to the Loopback.
- [ ] Verified the label table using `show mpls forwarding`.
