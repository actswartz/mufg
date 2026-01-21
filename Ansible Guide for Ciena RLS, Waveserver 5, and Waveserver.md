Ansible Guide for Ciena RLS, Waveserver 5, and Waveserver AiThis guide provides comprehensive instructions for automating Ciena optical platforms using Ansible. It distinguishes between the Waveserver family (which utilizes dedicated Ansible collections) and the 6500 Reconfigurable Line System (RLS) (which is automated using native NETCONF and OpenConfig YANG models).1. PrerequisitesBefore running playbooks, ensure your control node has the necessary software and libraries.System RequirementsAnsible Core: 2.12 or later recommended.Python: 3.8 or later.Python Libraries: The Ciena collections and standard NETCONF modules rely on ncclient and xmltodict to handle XML payloads and SSH transport.pip install ncclient xmltodict
2. Installing CollectionsYou need to install specific collections for Waveserver devices and the standard netcommon collection for RLS.# Install generic network collection (Required for RLS NETCONF)
ansible-galaxy collection install ansible.netcommon

# Install Ciena Waveserver 5 collection
ansible-galaxy collection install ciena.waveserver5

# Install Ciena Waveserver Ai collection
ansible-galaxy collection install ciena.waveserverai

# (Optional) Install SAOS 10 collection if your specific RLS software version supports it
ansible-galaxy collection install ciena.saos10
3. Inventory Configuration (hosts.ini)Define your inventory with the correct connection variables. Ciena devices typically use port 830 for NETCONF.[waveserver5]
ws5-01 ansible_host=192.168.10.11

[waveserver_ai]
wsai-01 ansible_host=192.168.10.12

[rls]
rls-01 ansible_host=192.168.10.13

[all:vars]
ansible_user=admin
ansible_password=YourSecurePassword
ansible_connection=netconf
ansible_port=830
ansible_network_os=auto 
# For RLS, 'auto' usually works. If issues arise, use 'default' to force raw NETCONF.
4. Automating Ciena Waveserver 5The ciena.waveserver5 collection abstracts the underlying API calls into Ansible modules.Example Playbook: waveserver5_complex.ymlThis playbook configures system details, provisions a client port with specific TTI (Trail Trace Identifier) settings, and gathers performance monitoring data.---
- name: Manage Ciena Waveserver 5
  hosts: waveserver5
  gather_facts: no
  collections:
    - ciena.waveserver5

  tasks:
    - name: Configure System Location and Contact
      waveserver5_system:
        config:
          location: "Data Center A - Row 4"
          contact: "NetOps Team"
        state: merged

    - name: Configure Client Port with TTI
      waveserver5_ports:
        config:
          - port_id: "1-1"
            admin_state: enabled
            description: "100G Uplink to Core"
            channels:
              - channel_id: 1
                id:
                  label: "Service-A"
                properties:
                  trace:
                    tx_sapi: "WS5-NODE-A"
                    tx_dapi: "WS5-NODE-B"
                    mismatch_fail_mode: "alarm-only"
        state: merged

    - name: Gather PMs (Performance Metrics)
      waveserver5_pm:
        gather_subset:
          - current
      register: pm_data

    - name: Show PM Data
      debug:
        var: pm_data
5. Automating Ciena Waveserver Ai (WSAI)The ciena.waveserverai collection handles the specific nuances of the Ai platform, particularly focusing on Transceivers (XCVRs) and Physical Termination Points (PTPs).Example Playbook: waveserver_ai_provisioning.ymlThis playbook configures a line-side transceiver for a specific modulation mode and enables the corresponding PTP.---
- name: Manage Ciena Waveserver Ai
  hosts: waveserver_ai
  gather_facts: no
  collections:
    - ciena.waveserverai

  tasks:
    - name: Configure Transceiver (XCVR) Mode
      # Sets the transceiver to 400G mode. 
      # Ensure the modem supports the selected mode.
      waveserverai_xcvrs:
        config:
          - xcvr_id: "1-1"
            properties:
              mode: "400GE" 
        state: merged

    - name: Provision PTP (Line Port) Frequency
      waveserverai_ptps:
        config:
          - ptp_id: "1-1"
            properties:
              frequency: 193100.00  # 193.1 THz
              tx_power: -2.0
            state:
              admin_state: enabled
        state: merged

    - name: Verify Configuration via Facts
      waveserverai_facts:
        gather_subset:
          - xcvrs
          - ptps
      register: ai_facts

    - name: Display Configured XCVR Mode
      debug:
        msg: "XCVR 1-1 Mode: {{ ai_facts.ansible_facts.ansible_net_xcvrs['1-1'].properties.mode }}"
6. Automating Ciena RLS (Reconfigurable Line System)RLS is a NETCONF-native platform. Unlike Waveserver, it is best automated using standard Ansible NETCONF modules by sending XML payloads that adhere to its YANG models. It heavily utilizes OpenConfig models alongside Ciena proprietary models.Key Concepts for RLSNamespaces: You must strictly define XML namespaces (xmlns).Wrappers: Payloads must be wrapped in <config> tags.Discovery: Use show netconf-yang schemas on the device CLI to find the correct namespace for a feature.Example Playbook: rls_advanced_netconf.ymlThis playbook covers three critical tasks: gathering system info via OpenConfig, configuring an IP interface (management), and retrieving optical alarms.---
- name: Ciena RLS Advanced Automation
  hosts: rls
  connection: netconf
  gather_facts: no
  collections:
    - ansible.netcommon

  tasks:
    # --- TASK 1: READ DATA (OpenConfig System) ---
    - name: Get System Info via OpenConfig
      netconf_get:
        filter: |
          <system xmlns="[http://openconfig.net/yang/system](http://openconfig.net/yang/system)">
            <config>
              <hostname/>
              <domain-name/>
            </config>
          </system>
      register: rls_system

    - name: Display Hostname
      debug:
        msg: "Device Hostname: {{ rls_system.result['data']['system']['config']['hostname'] }}"

    # --- TASK 2: CONFIGURATION (IP Interface) ---
    - name: Configure IP Interface (OpenConfig Interfaces)
      # This configures an IP on a logical interface, common for management 
      netconf_config:
        content: |
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="[http://openconfig.net/yang/interfaces](http://openconfig.net/yang/interfaces)">
              <interface>
                <name>ip-1</name>
                <config>
                  <name>ip-1</name>
                  <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:l3ipvlan</type>
                  <enabled>true</enabled>
                </config>
                <subinterfaces>
                  <subinterface>
                    <index>0</index>
                    <ipv4 xmlns="[http://openconfig.net/yang/interfaces/ip](http://openconfig.net/yang/interfaces/ip)">
                      <addresses>
                        <address>
                          <ip>10.0.0.50</ip>
                          <config>
                            <ip>10.0.0.50</ip>
                            <prefix-length>24</prefix-length>
                          </config>
                        </address>
                      </addresses>
                    </ipv4>
                  </subinterface>
                </interface>
              </interfaces>
            </config>
        commit: yes

    # --- TASK 3: SHELF MANAGEMENT (Ciena Proprietary) ---
    - name: Enable Shelf Admin State
      netconf_config:
        content: |
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <shelves xmlns="urn:ciena:params:xml:ns:yang:ciena-6500r-shelves">
              <shelf>
                <shelf-name>1</shelf-name>
                <admin-state>enabled</admin-state>
              </shelf>
            </shelves>
          </config>
        commit: yes

    # --- TASK 4: OPERATIONAL DATA (Alarms) ---
    - name: Retrieve Active Alarms
      netconf_rpc:
        rpc: "get"
        content: |
          <filter type="subtree">
             <active-alarm xmlns="urn:ciena:params:xml:ns:yang:ciena-pro-alarm"/>
          </filter>
      register: alarms

    - name: Show Alarm Count
      debug:
        msg: "Active Alarms: {{ alarms.output['data']['active-alarm'] | length }}"
      when: alarms.output['data']['active-alarm'] is defined
7. Troubleshooting"Access Denied" or Authentication Failures:Verify the user has the netconf role or privilege level.On RLS, check show user <username> to ensure the user is part of the NETCONF group.Namespace Errors (RLS):Symptom: rpc-error with bad-element or unknown-namespace.Fix: RLS is strict. If you omit xmlns="http://openconfig.net/...", the device will not recognize the tags. Verify the namespace against show netconf-yang schemas on the box.Collection Not Found:Ensure you ran ansible-galaxy collection install ... on the control node.Check ansible-galaxy collection list to verify versions.
