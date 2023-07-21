import tkinter as tk
import requests

def update_labels():
    url_str = "http://192.168.15.110:80/"  # Update with your server's IP address
    try:
        response = requests.get(url_str)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                if "Temperature:" in line:
                    temperature_label.config(text=line)
                elif "Photoresistor Value:" in line:
                    photoresistor_label.config(text=line)
                elif "Object Count:" in line:
                    count_label.config(text=line)
                elif "Your IP address:" in line:
                    ip_address_label.config(text=line)
        else:
            messagebox.showerror("Error", "HTTP connection failed: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        print(e)
        messagebox.showerror("Exception", "Exception occurred: " + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("HyeonJin Smart Factory")
    root.geometry("500x200")

    main_panel = tk.Frame(root)
    main_panel.pack(fill=tk.BOTH, expand=True)

    ip_address_label = tk.Label(main_panel, text="IP Address: ")
    temperature_label = tk.Label(main_panel, text="Temperature: ")
    photoresistor_label = tk.Label(main_panel, text="Photoresistor Value: ")
    count_label = tk.Label(main_panel, text="Object Count: ")

    label_font = ("Arial", 20)  # Increase font size
    ip_address_label.config(font=label_font)
    temperature_label.config(font=label_font)
    photoresistor_label.config(font=label_font)
    count_label.config(font=label_font)

    refresh_button = tk.Button(root, text="Check Condition", command=update_labels)
    refresh_button.pack(side=tk.BOTTOM)

    ip_address_label.pack()
    temperature_label.pack()
    photoresistor_label.pack()
    count_label.pack()

    root.mainloop()