# Lab 5: Dynamic Routing with OSPF

In this lab, you will use a Jinja2 template to deploy OSPF across your pod.

## Task: Create the Jinja2 Template
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

## Task: Create the Playbook `lab05_ospf.yml`
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

Run the playbook:
```bash
ansible-playbook -i inventory.yml lab05_ospf.yml
```