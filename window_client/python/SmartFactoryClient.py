import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timedelta
import json


def update_labels():
    url_str = "http://192.168.15.110:80/"  # Update with your server's IP address
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = requests.get(url_str)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                if "Temperature:" in line:
                    temp_value = line.split(': ')[1]
                    temperature_label.config(text=f'Internal factory temperature: {temp_value}')
                elif "Photoresistor Value:" in line:
                    photo_value = line.split(': ')[1]
                    photoresistor_label.config(text=f'Photoresistor Value: {photo_value}')
                elif "Object Count:" in line:
                    count_value = line.split(': ')[1]
                    count_label.config(text=f'Object Count: {count_value}')
                elif "Your IP address:" in line:
                    ip_value = line.split(': ')[1]
                    ip_address_label.config(text=f'IP Address: {ip_value}\nCurrent Datetime: {current_datetime}')
                elif "Factory Status:" in line:
                    factory_status = line.split(': ')[1]
                    factory_status_label.config(text=f'Factory Status: {factory_status}',
                                                fg=("green" if factory_status == "Running" else "red"))
                    update_label_visibility(factory_status)
                elif "Factory Operating Time: " in line:
                    operating_time = line.split(': ')[1]
                    operating_time_label.config(text=f'Factory Operating Time: {operating_time}')

        else:
            messagebox.showerror("Error", "HTTP connection failed: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        print(e)
        messagebox.showerror("Exception", "Exception occurred: " + str(e))

    current_weather, current_humidity = get_weather_and_humidity()
    ip_address_label.config(
        text=f"IP Address: {ip_value}\nCurrent Datetime: {current_datetime}\n{current_weather}\n{current_humidity}")

    root.after(1000, update_labels)


def get_weather_info(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    key = 'uKP0jRZGJnko8jBZliAO46iz2KbH7VvtJT74/2U5M/N2AsBjnoSS8xp36tTrVXXo4hIUQxhtMBnvXn3fBWYjlg=='

    now = datetime.now()
    base_date = int(now.strftime("%Y%m%d"))
    base_time = int((now - timedelta(hours=1)).strftime("%H00"))

    para = {
        'serviceKey': key,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    try:
        res = requests.get(url, params=para)
        res.raise_for_status()
        res_json = res.json()
        json.dumps(res_json, indent=2)

        if 'response' in res_json and 'body' in res_json['response'] and 'items' in res_json['response']['body']:
            items = res_json["response"]['body']['items']['item']
            filtered_items = [item for item in items if item['category'] in ['T1H', 'REH']]
            return filtered_items
        else:
            print("Unexpected result.")
            return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def get_weather_and_humidity():
    weather_info = get_weather_info(55, 124)  # Coordinates of Incheon City
    current_weather, current_humidity = "", ""

    if weather_info:
        for item in weather_info:
            category = item["category"]
            obsr_value = item["obsrValue"]
            if category == "T1H":
                current_weather = f"External factory temperature: {obsr_value}°C"
            elif category == "REH":
                current_humidity = f"External factory humidity: {obsr_value}%"

    return current_weather, current_humidity


def toggle_details():
    global show_details
    factory_status = factory_status_label.cget('text').split(': ')[1]

    if factory_status == "Stopped":
        messagebox.showwarning("Warning", "Factory is stopped. No details available.")
        return

    show_details = not show_details

    if show_details:
        details_button.config(text="Back")
    else:
        details_button.config(text="Check Factory Interior Condition")

    update_label_visibility(factory_status)


def update_label_visibility(factory_status):
    if show_details:
        if factory_status == "Running":
            temperature_label.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
            photoresistor_label.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
            count_label.grid(column=0, row=3, padx=5, pady=5, sticky='nsew')
            details_button.config(text="Back")
        else:  # Factory Status: Stopped
            temperature_label.grid_remove()
            photoresistor_label.grid_remove()
            count_label.grid_remove()
            details_button.config(text="Check Factory Interior Condition")
    else:
        temperature_label.grid_remove()
        photoresistor_label.grid_remove()
        count_label.grid_remove()
        details_button.config(text="Check Factory Interior Condition")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HyeonJin Smart Factory")

    main_panel = tk.Frame(root)
    main_panel.pack(fill=tk.BOTH, expand=True)

    show_details = False

    factory_status_label = tk.Label(main_panel, text="Factory Status")
    operating_time_label = tk.Label(main_panel, text="Factory Operating Time")
    ip_address_label = tk.Label(main_panel, text="IP Address")
    temperature_label = tk.Label(main_panel, text="")
    photoresistor_label = tk.Label(main_panel, text="")
    count_label = tk.Label(main_panel, text="")

    label_font = ("Arial", 20)
    label_font_small = ("Arial", 14)
    button_font = ("Arial", 16)

    factory_status_label.config(font=label_font)
    operating_time_label.config(font=label_font_small)
    ip_address_label.config(font=label_font_small)
    temperature_label.config(font=label_font_small)
    photoresistor_label.config(font=label_font_small)
    count_label.config(font=label_font_small)

    root.after(1000, update_labels)

    details_button = tk.Button(root, text="Check Factory Interior Condition", command=toggle_details, font=button_font)
    details_button.pack(side=tk.BOTTOM)

    factory_status_label.grid(column=0, row=0, columnspan=3, pady=5, sticky='nsew')
    operating_time_label.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
    ip_address_label.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')

    main_panel.grid_rowconfigure(2, weight=1)
    main_panel.grid_columnconfigure(0, weight=1)
    main_panel.grid_rowconfigure(0, weight=1)
    main_panel.grid_rowconfigure(1, weight=2)
    main_panel.grid_rowconfigure(2, weight=1)
    main_panel.grid_rowconfigure(3, weight=1)
    main_panel.grid_rowconfigure(4, weight=1)

    root.mainloop()
