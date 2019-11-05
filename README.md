FBX
===

About:

- It is a simple server which give access to multiple useful sensors. The output is a clean flattened json object perfect for [RESTful Sensor](https://www.home-assistant.io/integrations/rest/) integration. You can install this on a Freebox VM or on a raspberrypi for example.

Installation:

- `cd /opt`
- `git clone https://github.com/jr-k/freebox_home_assistant_probes`
- `cd freebox_home_assistant_probes`
- `cp app_infos.json.dist app_infos.json` (you can edit informations inside this file)
- `pip install -r requirements.txt` (or `pip3`)
- `python3 main.py`
- On first launch you'll have to grant access to the freebox by touching the check mark on the device
- You can check [http://localhost:9876/probes](http://localhost:9876/probes) (`localhost` or the hostname/ip of the device)

Output:

```json
{
  "system_temp_sw": 43,
  "system_user_main_storage": "Disque 1",
  "system_temp_cpu_cp_slave": 76,
  "system_mac": "AB:CD:EF:12:34:56",
  "system_box_flavor": "light",
  "system_temp_cpu_cp_master": 76,
  "system_fan_rpm": 1406,
  "system_temp_cpum": 43,
  "system_temp_cpu_ap": 65,
  "system_disk_status": "active",
  "system_temp_hdd2": 38,
  "system_temp_cpub": 47,
  "system_uptime": "3 heures 38 minutes 18 secondes",
  "system_uptime_val": 13098,
  "system_board_name": "fbxgw7r",
  "system_box_authenticated": true,
  "system_serial": "123402J5678901234",
  "system_firmware_version": "4.1.1",
  "connection_type": "ethernet",
  "connection_rate_down": 974,
  "connection_bytes_up": 50894648,
  "connection_ipv4_port_range": [0, 16383],
  "connection_rate_up": 1430,
  "connection_bandwidth_up": 600000000,
  "connection_ipv6": "1ab4:cdead:beef:934a::1",
  "connection_bandwidth_down": 10000000000,
  "connection_media": "ftth",
  "connection_state": "up",
  "connection_bytes_down": 445809117,
  "connection_ipv4": "12.34.56.78",
  "disk0_type": "sata",
  "disk0_total_bytes": 1000000000000,
  "disk0_connector": 2,
  "disk0_id": 1000,
  "disk0_active_duration": 0,
  "disk0_idle_duration": 20,
  "disk0_state": "enabled",
  "disk0_idle": true,
  "disk0_spinning": false,
  "disk0_model": "ST1000LM048-2E7172",
  "disk0_table_type": "gpt",
  "disk0_temp": 38,
  "disk0_serial": "AB100ABC",
  "disk0_firmware": "0001",
  "disk0_partition0_fstype": "ext4",
  "disk0_partition0_total_bytes": 984370000000,
  "disk0_partition0_label": "Disque 1",
  "disk0_partition0_id": 1001,
  "disk0_partition0_internal": false,
  "disk0_partition0_fsck_result": "no_run_yet",
  "disk0_partition0_state": "mounted",
  "disk0_partition0_disk_id": 1000,
  "disk0_partition0_free_bytes": 977610000000,
  "disk0_partition0_used_bytes": 6740000000,
  "disk0_partition0_path": "A1Sab1F1GTBz"
}
```

HomeAssistant Sensor Configuration:

```yaml
sensor:
  - platform: rest
    resource: http://your_server_host:9876/probes
    name: FREEBOX sensors
    value_template: '{{ value_json.connection_ipv4 }}'
    scan_interval: 10
    json_attributes:
      - system_temp_sw
      - system_user_main_storage
      - system_temp_cpu_cp_slave
      - system_mac
      - system_box_flavor
      - system_temp_cpu_cp_master
      - system_fan_rpm
      - system_temp_cpum
      - system_temp_cpu_ap
      - system_disk_status
      - system_temp_hdd2
      - system_temp_cpub
      - system_uptime
      - system_uptime_val
      - system_board_name
      - system_box_authenticated
      - system_serial
      - system_firmware_version
      - connection_type
      - connection_rate_down
      - connection_bytes_up
      - connection_ipv4_port_range
      - connection_rate_up
      - connection_bandwidth_up
      - connection_ipv6
      - connection_bandwidth_down
      - connection_media
      - connection_state
      - connection_bytes_down
      - connection_ipv4
      - disk0_type
      - disk0_total_bytes
      - disk0_connector
      - disk0_id
      - disk0_active_duration
      - disk0_idle_duration
      - disk0_state
      - disk0_idle
      - disk0_spinning
      - disk0_model
      - disk0_table_type
      - disk0_temp
      - disk0_serial
      - disk0_firmware
      - disk0_partition0_fstype
      - disk0_partition0_total_bytes
      - disk0_partition0_label
      - disk0_partition0_id
      - disk0_partition0_internal
      - disk0_partition0_fsck_result
      - disk0_partition0_state
      - disk0_partition0_disk_id
      - disk0_partition0_free_bytes
      - disk0_partition0_used_bytes
      - disk0_partition0_path
```

Start Server API as a service (start on boot with `systemd`):

```
sudo nano /lib/systemd/system/freebox-probes.service
```

- Change the configuration file according to your system, especially the `ExecStart` value
```
[Unit]
Description=Freebox Probes
Wants=network-online.target
After=network.target

[Service]
WorkingDirectory=/opt/freebox_home_assistant_probe
ExecStart=/usr/bin/python3 /opt/freebox_home_assistant_probes/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
- Restart the daemon
`sudo systemctl daemon-reload`

- Enable the service with
`sudo systemctl enable freebox-probes`

- Start the service with
`sudo systemctl start freebox-probes`

- That's it, the server is now running in background silently and will be started automatically if you reboot.

