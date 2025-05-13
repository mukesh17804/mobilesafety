# 🔌 Mobile Charging Safety – UI Blocking System

A Python-based solution using **Tkinter** to enhance mobile device safety by **blocking user access during charging**. This project aims to prevent risks like **battery overheating, electrical hazards, and unauthorized access** by enforcing safe charging practices.

## 🚀 Features

- 🔋 **Charging Detection** – Automatically detects when the device is charging.
- 🛡️ **UI Blocking** – Locks the user interface while charging.
- 🚨 **Emergency Notification Support** – Allows emergency calls/alerts to bypass the block.
- 🔊 **Beep Alerts** – Notifies the user to unplug the charger in case of emergencies.
- 🔓 **Full Access Restoration** – Automatically restores access once charging is complete.
- 🖥️ **Built with Tkinter** – Simple and clean GUI for user notifications.

---

## 📷 Screenshot

> (Add your project image or UI screenshot here)

---

## 🧠 How It Works

1. The system continuously monitors the device's charging status.
2. If charging is detected:
   - A full-screen Tkinter window blocks the UI.
   - The user cannot close the window unless the charger is unplugged.
3. If an emergency (e.g., incoming call) is detected:
   - A beep alert prompts the user to unplug and access the device.
4. Once unplugged:
   - The UI lock is automatically removed.

---

## 🛠️ Requirements

- Python 3.6+
- Tkinter (comes pre-installed with Python)
- Linux (for detecting battery status using `/sys/class/power_supply/BAT0/status`)
  - Windows support can be added separately.

---

## 💻 Installation & Run

```bash
git clone https://github.com/your-username/mobile-charging-safety.git
cd mobile-charging-safety
python3 ui_blocking.py
