import requests
import tkinter as tk

# 백엔드
def update_labels():

    web_server_url = "http://192.168.15.245:80"

    response = requests.get(web_server_url)
    data = response.text
    # print(data)
    lines = data.split("\n")  # lines의 2번방에서 ':' 다음에 나온 아이피만 잘라서 쓰고싶음
    # print(lines)

    ip_address = ''
    if len(lines) >= 4:
        ip_address = lines[2].split(": ")[1]
    # print(f"아이피 주소: {ip_address}")
    # print(lines[3])

    lbl_ip.config(text=f"아이피 주소: {ip_address}")
    lbl_temperature.config(text=lines[3])


# 프론트엔드 -> create gui component
current_temperature_condition = tk.Tk()
current_temperature_condition.title("Inha Smart Factory")
current_temperature_condition.geometry("400x200")
lbl_ip = tk.Label(current_temperature_condition, text="IP address: ")
lbl_temperature = tk.Label(current_temperature_condition, text="")
btn_check_temperature = tk.Button(current_temperature_condition, text="Check Temperature!", command=update_labels)

# layout
lbl_ip.grid(row=0, column=0)
lbl_temperature.grid(row=0, column=1)
btn_check_temperature.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
current_temperature_condition.mainloop()



