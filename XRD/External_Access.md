# XRD Lab External Access Guide

This document provides the mapping for external SSH access to the XRd nodes from the public internet.

## Connection Details
- **Public IP:** `136.243.78.83`
- **Default Credentials:** To be configured (Recommended: `clab` / `800-ePlus`)

## Port Mapping Table

| Pod | Node | Internal IP | External Port | SSH Command |
| :--- | :--- | :--- | :--- | :--- |
| **Pod 1** | p1-xr1 | 172.30.30.11 | **31011** | `ssh -4 -p 31011 clab@136.243.78.83` |
| **Pod 1** | p1-xr2 | 172.30.30.12 | **31012** | `ssh -4 -p 31012 clab@136.243.78.83` |
| **Pod 2** | p2-xr1 | 172.30.30.21 | **31021** | `ssh -4 -p 31021 clab@136.243.78.83` |
| **Pod 2** | p2-xr2 | 172.30.30.22 | **31022** | `ssh -4 -p 31022 clab@136.243.78.83` |
| **Pod 3** | p3-xr1 | 172.30.30.31 | **31031** | `ssh -4 -p 31031 clab@136.243.78.83` |
| **Pod 3** | p3-xr2 | 172.30.30.32 | **31032** | `ssh -4 -p 31032 clab@136.243.78.83` |
| **Pod 4** | p4-xr1 | 172.30.30.41 | **31041** | `ssh -4 -p 31041 clab@136.243.78.83` |
| **Pod 4** | p4-xr2 | 172.30.30.42 | **31042** | `ssh -4 -p 31042 clab@136.243.78.83` |
| **Pod 5** | p5-xr1 | 172.30.30.51 | **31051** | `ssh -4 -p 31051 clab@136.243.78.83` |
| **Pod 5** | p5-xr2 | 172.30.30.52 | **31052** | `ssh -4 -p 31052 clab@136.243.78.83` |

> **Note:** If you encounter "Network is unreachable," ensure you are using the `-4` flag to force the connection over IPv4.

## Setup Instructions
Before these ports become active, you must log into each container via Docker console and configure the management interface:

1. `docker exec -it clab-xrd-lab-<node_name> xr`
2. Configure the following:
   ```ios
   conf t
    username clab group root-lr group cisco-support secret 800-ePlus
    interface MgmtEth0/RP0/CPU0/0
     ipv4 address <Internal_IP> 255.255.255.0
     no shut
    commit
   ```
