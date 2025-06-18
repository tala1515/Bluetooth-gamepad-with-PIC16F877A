import serial
import threading
import tkinter as tk

# ---- Serial connection settings ----
COM_PORT = "COM4"
BAUD_RATE = 9600

data = {
    'J1X': 64, 'J1Y': 64,
    'J2X': 64, 'J2Y': 64,
    'B1': 0, 'B2': 0,
    'SND': 1
}


# ---- Reading from serial port ----
def read_serial():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("J1X"):
                parts = line.split()
                for part in parts:
                    key, val = part.split(":")
                    val = int(val)
                    if key in data:
                        data[key] = val

                # Buzzer kontrolü
                if data['SND'] == 1 and (data['B1'] == 0 or data['B2'] == 0):
                    buzzer_status.config(text="Buzzer: ON", fg="lime")
                elif data['SND'] == 0:
                    buzzer_status.config(text="Buzzer: OFF (Muted)", fg="gray")
                else:
                    buzzer_status.config(text="Buzzer: OFF", fg="red")

        except Exception as e:
            print(f"Serial Error: {e}")


# ---- update GUI ----
def update_gui():
    j1_label.config(text=f"Joystick R → X={data['J1X']-128}  Y={128-data['J1Y']}")
    j2_label.config(text=f"Joystick L → X={128-data['J2X']}  Y={data['J2Y']-128}")

    btn1_indicator.config(bg="lime green" if data['B1'] == 0 else "red")
    btn2_indicator.config(bg="lime green" if data['B2'] == 0 else "red")

    # Joystick 1 coord
    canvas1.delete("all")
    cx1, cy1 = data['J1X'], data['J1Y']
    canvas1.create_oval(cx1-4, cy1-4, cx1+4, cy1+4, fill="cyan", outline="")

    # Joystick 2 coord
    canvas2.delete("all")
    cx2, cy2 = data['J2X'], data['J2Y']
    canvas2.create_oval(256-cx2-4, 256-cy2-4, 256-cx2+4, 256-cy2+4, fill="orange", outline="")

    root.after(20, update_gui)

# ---- Main window----
root = tk.Tk()
root.title("Joystick Control Panel")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.configure(bg="black")
canvas_frame = tk.Frame(root, bg="black")
canvas_frame.pack(pady=10)

# ---- Main label ----
header = tk.Label(root, text="Joystick Control System", font=("Arial", 16, "bold"), fg="white", bg="black")
header.pack(pady=10)

# ---- Sound status ----
sound_status = tk.Label(root, text="Sound: Controlled by Device", font=("Arial", 11), bg="black", fg="white")
sound_status.pack()

buzzer_status = tk.Label(root, text="Buzzer: OFF", font=("Arial", 12, "bold"), bg="black", fg="red")
buzzer_status.pack(pady=10)

# ---- Joystick 1 ----
frame1 = tk.LabelFrame(canvas_frame, text="Joystick R", fg="white", bg="black", font=("Arial", 10, "bold"))
frame1.pack(side="right", padx=10, pady=5, fill="x")

j1_label = tk.Label(frame1, text="", font=("Courier", 12), bg="black", fg="cyan")
j1_label.pack()

canvas1 = tk.Canvas(frame1, width=256, height=256, bg="black", highlightthickness=1, highlightbackground="white")
canvas1.pack(pady=5)

btn1_frame = tk.Frame(frame1, bg="black")
btn1_frame.pack()
tk.Label(btn1_frame, text="Button:", fg="white", bg="black").pack(side="left")
btn1_indicator = tk.Label(btn1_frame, text=" ", bg="red", width=3)
btn1_indicator.pack(side="left")

# ---- Joystick 2 ----
frame2 = tk.LabelFrame(canvas_frame, text="Joystick L", fg="white", bg="black", font=("Arial", 10, "bold"))
frame2.pack(side="left", padx=10, pady=5, fill="x")

j2_label = tk.Label(frame2, text="", font=("Courier", 12), bg="black", fg="orange")
j2_label.pack()

canvas2 = tk.Canvas(frame2, width=256, height=256, bg="black", highlightthickness=1, highlightbackground="white")
canvas2.pack(pady=5)

btn2_frame = tk.Frame(frame2, bg="black")
btn2_frame.pack()
tk.Label(btn2_frame, text="Button:", fg="white", bg="black").pack(side="left")
btn2_indicator = tk.Label(btn2_frame, text=" ", bg="red", width=3)
btn2_indicator.pack(side="left")

# ---- Init serial connection ----
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"{COM_PORT} connected.")
except Exception as e:
    print(f"{COM_PORT} connection failed: {e}")
    exit()

# ---- Threading and loop ----
threading.Thread(target=read_serial, daemon=True).start()
root.after(20, update_gui)
root.mainloop()