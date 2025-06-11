# Mac-Address-Changer

This repository contains a small Python script to change the MAC address of a
network interface on Linux systems.

## Usage

Run the script with root privileges and provide the interface name. A custom
MAC address can be specified with `--mac`; otherwise a random address is used.

```bash
sudo python3 mac_changer.py eth0 --mac 00:11:22:33:44:55
```

