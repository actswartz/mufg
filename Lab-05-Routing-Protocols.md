# Lab 5: Dynamic Routing with OSPF

Now that your interfaces have IPs, it's time to enable routing so the devices can talk to each other across the network.

## 🧠 Core Concept: Jinja2 Templating
Sometimes, a standard Ansible module doesn't cover every specific command you need. In these cases, we use **Jinja2 Templates**. 
A template is a text file that contains your Cisco commands with "placeholders" for variables. 

## Task 1: Create the Jinja2 Template 📄

Create a folder named `templates`: `mkdir templates`
Create `templates/ospf_config.j2`:
```text
router ospf 1
 router-id {{ ospf.router_id }}
 log-adjacency-changes
{% for net in ospf.networks %}
 network {{ net.network }} {{ net.wildcard }} area {{ net.area }}
{% endfor %}
{% for intf in l3_interfaces %}
 {% if intf.name != 'Ethernet0/0' %}
 interface {{ intf.name }}
  ip ospf 1 area 0
 {% endif %}
{% endfor %}
```

### 🔍 Breakdown of Template Logic:
*   **`{{ variable }}`**: Inserts a value (like the Router ID).
*   **`{% for ... %}`**: A loop. It will create a `network` line for every network listed in your inventory.
*   **`{% if ... %}`**: A conditional. We skip `Ethernet0/0` because that is our management interface and we don't want OSPF running on it.

## Task 2: Create the `lab05_ospf.yml` Playbook

```yaml
---
- name: Lab 5 - OSPF Configuration
  hosts: routers
  gather_facts: false
  tasks:
    - name: Generate and Apply OSPF Config
      cisco.ios.ios_config:
        src: templates/ospf_config.j2
```

### 🔍 How it works:
The `ios_config` module takes your template, fills in the variables for each specific router, and sends the resulting list of commands to the device.

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab05_ospf.yml
```
