import psutil
import time
import threading
import sys
from PIL import Image, ImageDraw
import pystray

LIMIT = 80
LOWER_LIMIT = 30
CHECK_INTERVAL = 5

notified = False

def create_battery_icon(percentage, is_charging):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outline_color = "#00BFFF" if is_charging else "white"

    draw.rectangle([18, 14, 46, 58], outline=outline_color, width=3)
    draw.rectangle([26, 8, 38, 14], fill=outline_color)

    fill_amount = int((percentage / 100) * 38)
    if percentage >= LIMIT or percentage <= LOWER_LIMIT:
        color = "#FF4444"
    else:
        color = "#44FF88"

    if fill_amount > 0:
        draw.rectangle([21, 55 - fill_amount, 43, 55], fill=color)

    if is_charging:
        lightning_points = [(34, 20), (24, 35), (30, 35), (26, 52), (40, 31), (34, 31)]
        draw.polygon(lightning_points, fill="yellow", outline="black")

    return img

def monitor_battery(icon):
    global notified

    while True:
        battery = psutil.sensors_battery()

        if battery is None:
            icon.title = "Battery not found"
            time.sleep(CHECK_INTERVAL)
            continue

        percentage = int(battery.percent)
        is_charging = battery.power_plugged

        status = "🔌 Charging" if is_charging else "🔋 On Battery"
        icon.title = f"Battery: {percentage}% — {status}"
        icon.icon = create_battery_icon(percentage, is_charging)

        if is_charging and percentage >= LIMIT and not notified:
            icon.notify(f"Battery reached {percentage}%! Please unplug.", title="🔋 Upper Limit Warning")
            notified = True

        if not is_charging and percentage <= LOWER_LIMIT and not notified:
            icon.notify(f"Battery dropped to {percentage}%! Please plug in.", title="🪫 Lower Limit Warning")
            notified = True

        if LOWER_LIMIT < percentage < LIMIT:
            notified = False

        time.sleep(CHECK_INTERVAL)

def change_upper_limit(icon, item):
    global LIMIT, notified
    LIMIT = 90 if LIMIT == 80 else 80
    notified = False
    icon.notify(f"Upper charge warning limit changed to {LIMIT}%.", title="Battery Monitor")
    
    battery = psutil.sensors_battery()
    if battery is not None:
        percentage = int(battery.percent)
        is_charging = battery.power_plugged
        icon.icon = create_battery_icon(percentage, is_charging)

def change_lower_limit(icon, item):
    global LOWER_LIMIT, notified
    LOWER_LIMIT = 30 if LOWER_LIMIT == 20 else 20
    notified = False
    icon.notify(f"Lower charge warning limit changed to {LOWER_LIMIT}%.", title="Battery Monitor")
    
    battery = psutil.sensors_battery()
    if battery is not None:
        percentage = int(battery.percent)
        is_charging = battery.power_plugged
        icon.icon = create_battery_icon(percentage, is_charging)

def quit_app(icon, item):
    icon.stop()
    sys.exit(0)

def main():
    initial_icon = create_battery_icon(50, False)

    menu = pystray.Menu(
        pystray.MenuItem("Battery Monitor", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(lambda item: f"Change Upper Limit ({'90% / 80%' if LIMIT == 90 else '80% / 90%'})", change_upper_limit),
        pystray.MenuItem(lambda item: f"Change Lower Limit ({'30% / 20%' if LOWER_LIMIT == 30 else '20% / 30%'})", change_lower_limit),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", quit_app),
    )

    icon = pystray.Icon(
        name="BatteryMonitor",
        icon=initial_icon,
        title="Battery Monitor — Starting...",
        menu=menu,
    )

    t = threading.Thread(target=monitor_battery, args=(icon,), daemon=True)
    t.start()

    icon.run()

if __name__ == "__main__":
    main()
