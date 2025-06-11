#!/usr/bin/env python3
"""Utility to change the MAC address of a network interface."""

import argparse
import random
import re
import subprocess


def get_current_mac(interface: str) -> str | None:
    """Return the current MAC address for the given interface."""
    try:
        output = subprocess.check_output([
            "ip",
            "link",
            "show",
            interface,
        ], encoding="utf-8")
    except subprocess.CalledProcessError:
        return None
    match = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", output)
    return match.group(1).lower() if match else None


def change_mac(interface: str, new_mac: str) -> None:
    """Change the MAC address for the given interface."""
    subprocess.check_call(["sudo", "ip", "link", "set", "dev", interface, "down"])
    subprocess.check_call([
        "sudo",
        "ip",
        "link",
        "set",
        "dev",
        interface,
        "address",
        new_mac,
    ])
    subprocess.check_call(["sudo", "ip", "link", "set", "dev", interface, "up"])


def random_mac() -> str:
    """Generate a random MAC address."""
    hex_digits = "0123456789abcdef"
    return ":".join(
        random.choice(hex_digits) + random.choice(hex_digits) for _ in range(6)
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Change MAC address of a network interface."
    )
    parser.add_argument(
        "interface",
        help="Network interface to modify, e.g. eth0",
    )
    parser.add_argument(
        "--mac",
        help="MAC address to assign; if omitted, a random address is used",
    )
    args = parser.parse_args()

    new_mac = args.mac if args.mac else random_mac()

    current = get_current_mac(args.interface)
    print(f"Current MAC for {args.interface}: {current}")

    print(f"Changing MAC for {args.interface} to {new_mac}...")
    change_mac(args.interface, new_mac)

    updated = get_current_mac(args.interface)
    if updated == new_mac.lower():
        print(f"Successfully changed MAC to {updated}")
    else:
        print("Failed to change MAC address")


if __name__ == "__main__":
    main()
