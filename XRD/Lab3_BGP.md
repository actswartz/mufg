# Lab 3: BGP Scalability (eBGP & Route Policies)

## Lab Overview
In this lab, you will connect your two routers via **BGP (Border Gateway Protocol)**. BGP is the protocol that runs the internet, but in IOS-XR, it has a "Security First" design that behaves differently than traditional IOS.

By the end of this lab, you will have:
1. Mastered **RPL (Route Policy Language)**—the backbone of XR filtering.
2. Established an eBGP session between `xr1` and `xr2`.
3. Learned the "Default Deny" nature of BGP in XR.
4. Verified the exchange of prefixes between autonomous systems.

---

## Part 1: Route Policy Language (RPL) ️

### What is happening?
In traditional IOS, if you have no filters, BGP accepts everything. In IOS-XR, BGP will **reject everything** unless you explicitly apply a policy. We will create a "Pass-All" policy to allow our traffic.

### The Purpose
RPL is a highly structured, programming-like language. It is much more powerful and efficient than using complex access-lists and route-maps for large-scale filtering.

### ️ Step-by-Step:
Create a simple "Allow-All" policy on **both routers**:
```ios
conf t
 route-policy PASS_ALL
 done
 !
 commit
```
> **Note:** The `done` keyword simply means "Accept." Without this policy, your BGP neighbor will stay `Up`, but you will see **0 prefixes** learned.

---

## Part 2: Configuring eBGP 

### What is happening?
We will configure **Router 1** in AS 65001 and **Router 2** in AS 65002. They will peer using the physical link IPs we configured in Lab 1.

### ️ Step-by-Step:
Configure BGP on **Router 1**:
```ios
conf t
 router bgp 65001
 address-family ipv4 unicast
 !
 neighbor 10.1.1.2
  remote-as 65002
  address-family ipv4 unicast
  route-policy PASS_ALL in
  route-policy PASS_ALL out
  !
 commit
```

*Repeat the steps on **Router 2**, using `remote-as 65001` and targeting IP `10.1.1.1`.*

---

## Part 3: Verification 

#### Command: `show bgp ipv4 unicast summary`
This shows the status of your BGP neighbors.

**Sample Output:**
```text
RP/0/RP0/CPU0:p1-xr1# show bgp ipv4 unicast summary
BGP router identifier 1.1.1.1, local AS number 65001
Neighbor    Spk  AS MsgRcvd MsgSent  TblVer InQ OutQ Up/Down State/PfxRcd
10.1.1.2     0 65002   12   15    5  0  0 00:08:42      1
```
> **Note:** If "State/PfxRcd" shows a number, the session is active! If it says "Idle" or "Active" (confusingly), it is down.

#### Command: `show bgp ipv4 unicast neighbors 10.1.1.2 advertised-routes`
Check what routes you are sending to your neighbor.

---

## Summary Checklist
- [ ] Created the `PASS_ALL` route policy.
- [ ] Configured the BGP process and address-family.
- [ ] Applied the route policy to both `in` and `out` directions.
- [ ] Verified the BGP session state is `Established`.
