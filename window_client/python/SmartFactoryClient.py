import tkinter as tk
from tkinter import messagebox
import requests
import datetime


def update_labels():
    url_str = "http://192.168.0.75:80/"  # Update with your server's IP address
    try:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = requests.get(url_str)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                if "Temperature:" in line:
                    temp_value = line.split(': ')[1]
                    temperature_label.config(text=f'Temperature: {temp_value}')
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

        else:
            messagebox.showerror("Error", "HTTP connection failed: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        print(e)
        messagebox.showerror("Exception", "Exception occurred: " + str(e))

    root.after(1000, update_labels)


def toggle_details():
    global show_details
    factory_status = factory_status_label.cget('text').split(': ')[1]

    if factory_status == "Stopped":
        messagebox.showwarning("Warning", "Factory is stopped. No details available.")
        return

    show_details = not show_details

    if show_details:
        details_button.config(text="Hide Condition")
    else:
        details_button.config(text="Check Condition")

    update_label_visibility(factory_status)


def update_label_visibility(factory_status):
    if show_details:
        if factory_status == "Running":
            temperature_label.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
            photoresistor_label.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
            count_label.grid(column=0, row=3, padx=5, pady=5, sticky='nsew')
            details_button.config(text="Hide Condition")
        else:  # Factory Status: Stopped
            temperature_label.grid_remove()
            photoresistor_label.grid_remove()
            count_label.grid_remove()
            details_button.config(text="Check Condition")
    else:
        temperature_label.grid_remove()
        photoresistor_label.grid_remove()
        count_label.grid_remove()
        details_button.config(text="Check Condition")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HyeonJin Smart Factory")

    main_panel = tk.Frame(root)
    main_panel.pack(fill=tk.BOTH, expand=True)

    show_details = False

    factory_status_label = tk.Label(main_panel, text="Factory Status")
    ip_address_label = tk.Label(main_panel, text="IP Address")
    temperature_label = tk.Label(main_panel, text="")
    photoresistor_label = tk.Label(main_panel, text="")
    count_label = tk.Label(main_panel, text="")

    label_font = ("Arial", 20)
    label_font_small = ("Arial", 14)
    button_font = ("Arial", 16)

    factory_status_label.config(font=label_font)
    ip_address_label.config(font=label_font_small)
    temperature_label.config(font=label_font)
    photoresistor_label.config(font=label_font)
    count_label.config(font=label_font)

    root.after(1000, update_labels)

    details_button = tk.Button(root, text="Check Condition", command=toggle_details, font=button_font)
    details_button.pack(side=tk.BOTTOM)

    factory_status_label.grid(column=0, row=0, columnspan=3, pady=5, sticky='nsew')
    ip_address_label.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')

    main_panel.grid_rowconfigure(2, weight=1)
    main_panel.grid_columnconfigure(0, weight=1)
    main_panel.grid_rowconfigure(0, weight=1)
    main_panel.grid_rowconfigure(1, weight=2)
    main_panel.grid_rowconfigure(2, weight=1)
    main_panel.grid_rowconfigure(3, weight=1)
    main_panel.grid_rowconfigure(4, weight=1)

    root.mainloop()
