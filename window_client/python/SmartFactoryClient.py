import tkinter as tk
from tkinter import messagebox
import requests


def update_labels():
    url_str = "http://192.168.0.75:80/"  # Update with your server's IP address
    try:
        response = requests.get(url_str)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                if "Temperature:" in line:
                    temp_value = line.split(': ')[1]
                    temperature_label.config(text=f'Temperature\n\n{temp_value}')
                elif "Photoresistor Value:" in line:
                    photo_value = line.split(': ')[1]
                    photoresistor_label.config(text=f'Photoresistor Value\n\n{photo_value}')
                elif "Object Count:" in line:
                    count_value = line.split(': ')[1]
                    count_label.config(text=f'Object Count\n\n{count_value}')
                elif "Your IP address:" in line:
                    ip_value = line.split(': ')[1]
                    ip_address_label.config(text=f'IP Address\n\n{ip_value}')
        else:
            messagebox.showerror("Error", "HTTP connection failed: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        print(e)
        messagebox.showerror("Exception", "Exception occurred: " + str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HyeonJin Smart Factory")
    root.state('zoomed')

    main_panel = tk.Frame(root)
    main_panel.pack(fill=tk.BOTH, expand=True)

    ip_address_label = tk.Label(main_panel, text="IP Address")
    temperature_label = tk.Label(main_panel, text="Temperature")
    photoresistor_label = tk.Label(main_panel, text="Light")
    count_label = tk.Label(main_panel, text="Object Count")

    label_font = ("Arial", 20)
    ip_address_label.config(font=label_font)
    temperature_label.config(font=label_font)
    photoresistor_label.config(font=label_font)
    count_label.config(font=label_font)

    refresh_button = tk.Button(root, text="Check Condition", command=update_labels)
    refresh_button.pack(side=tk.BOTTOM)

    ip_address_label.grid(column=0, row=0, sticky='nsew')
    temperature_label.grid(column=1, row=0, sticky='nsew')
    photoresistor_label.grid(column=0, row=1, sticky='nsew')
    count_label.grid(column=1, row=1, sticky='nsew')

    main_panel.grid_columnconfigure(0, weight=1)
    main_panel.grid_columnconfigure(1, weight=1)
    main_panel.grid_rowconfigure(0, weight=1)
    main_panel.grid_rowconfigure(1, weight=1)

    root.mainloop()
