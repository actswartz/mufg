Ciena Automation with AnsibleA comprehensive guide for automating Ciena optical platforms. This repository covers the Waveserver family (utilizing dedicated collections) and the 6500 Reconfigurable Line System (RLS) (utilizing native NETCONF/YANG).Table of ContentsPrerequisitesInstallationInventory SetupWaveserver 5 AutomationWaveserver Ai AutomationRLS Automation (NETCONF)TroubleshootingPrerequisitesBefore running playbooks, ensure your control node meets the following requirements.Ansible Core: 2.12 or later.Python: 3.8 or later.Libraries: ncclient and xmltodict are required for XML payload handling.pip install ncclient xmltodict
InstallationInstall the required Ansible collections from Galaxy.Device FamilyCollectionMethodRLS / 6500ansible.netcommonStandard NETCONFWaveserver 5ciena.waveserver5REST/API ModulesWaveserver Aiciena.waveserveraiREST/API Modules# 1. Install generic network collection (Required for RLS NETCONF)
ansible-galaxy collection install ansible.netcommon

# 2. Install Ciena Waveserver 5 collection
ansible-galaxy collection install ciena.waveserver5

# 3. Install Ciena Waveserver Ai collection
ansible-galaxy collection install ciena.waveserverai

# 4. (Optional) SAOS 10 support
ansible-galaxy collection install ciena.saos10
Inventory SetupDefine your hosts.ini with connection variables. Note that Ciena devices typically listen on port 830 for NETCONF.[waveserver5]
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
# Tip: For RLS, if 'auto' fails, use 'default' to force raw NETCONF.
Waveserver 5 AutomationThe ciena.waveserver5 collection abstracts the API into Ansible modules.Example: System & Port ConfigurationFile: waveserver5_complex.yml---
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

    - name: Gather PMs
      waveserver5_pm:
        gather_subset:
          - current
      register: pm_data

    - name: Debug PM Data
      debug:
        var: pm_data
Waveserver Ai AutomationThe ciena.waveserverai collection handles specific nuances like Transceivers (XCVRs) and PTPs.Example: Provisioning XCVR & PTPFile: waveserver_ai_provisioning.yml---
- name: Manage Ciena Waveserver Ai
  hosts: waveserver_ai
  gather_facts: no
  collections:
    - ciena.waveserverai

  tasks:
    - name: Configure Transceiver (XCVR) Mode
      waveserverai_xcvrs:
        config:
          - xcvr_id: "1-1"
            properties:
              mode: "400GE"
        state: merged

    - name: Provision PTP Frequency
      waveserverai_ptps:
        config:
          - ptp_id: "1-1"
            properties:
              frequency: 193100.00  # 193.1 THz
              tx_power: -2.0
            state:
              admin_state: enabled
        state: merged

    - name: Verify Configuration
      waveserverai_facts:
        gather_subset:
          - xcvrs
          - ptps
      register: ai_facts

    - name: Display Mode
      debug:
        msg: "XCVR 1-1 Mode: {{ ai_facts.ansible_facts.ansible_net_xcvrs['1-1'].properties.mode }}"
RLS Automation (NETCONF)RLS is a NETCONF-native platform utilizing OpenConfig and Ciena proprietary YANG models.Important: RLS is strict about XML namespaces (xmlns). Always verify the namespace using show netconf-yang schemas on the device.Example: Advanced Configuration (IP & Shelf)File: rls_advanced_netconf.yml---
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
TroubleshootingCommon IssuesAccess Denied / Authentication FailureCause: User lacks NETCONF privileges.Fix: Check show user <username> on the device. Ensure the user is in the netconf group.Namespace Errors (RLS)Symptom: rpc-error with bad-element or unknown-namespace.Fix: RLS is strict. Omitting xmlns="http://openconfig.net/..." will cause failure.Debug: Use show netconf-yang schemas on the CLI to confirm the exact URI.Collection Not FoundFix: Run ansible-galaxy collection list to ensure Ciena collections are installed.Disclaimer: This guide is for educational purposes. Always test automation in a lab environment before deploying to production Ciena nodes.
