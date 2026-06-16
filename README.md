# Battery Monitor

A lightweight Windows system tray application that monitors battery status in real time and notifies users when configurable charge or discharge thresholds are reached.

## Why?

Many laptop users prefer to keep their battery within a specific charge range instead of leaving it at 100% for long periods. BatteryMonitor provides customizable notifications when upper or lower battery thresholds are reached, helping users manage charging habits more easily.

## Features

- Real-time battery monitoring
- Dynamic tray icon with battery level indicator
- Charging status visualization
- Configurable upper charge limit (80% / 90%)
- Configurable lower battery limit (20% / 30%)
- Desktop notifications for battery thresholds
- Lightweight and runs in the system tray

## Requirements

- Python 3.10+
- psutil
- pystray
- Pillow

## Installation

```bash
pip install psutil pystray pillow
python battery_monitor.py
