import tkinter as tk
import random
import time
import threading
import winsound

# Sanakirja maailmanennätysajoille
maailmanennatykset = {
    1920: {'aika': 10.6, 'nimi': 'Charlie Paddock'},
    1930: {'aika': 10.3, 'nimi': 'Percy Williams'},
    1988: {'aika': 9.79, 'nimi': 'Ben Johnson'},
    2009: {'aika': 9.58, 'nimi': 'Usain Bolt'},
}

# Juoksijoiden ominaisuudet
ernesti_speed = random.uniform(10.0, 15.0)
kernesti_speed = random.uniform(10.0, 15.0)

# Harjoittelun kehityksen seuranta (sekuntia/100m)
kehitys = {
    "Ernesti": ernesti_speed,
    "Kernesti": kernesti_speed
}

# Tkinter käyttöliittymä
root = tk.Tk()
root.title("Ernestin ja Kernestin Juoksu")

canvas = tk.Canvas(root, width=600, height=200, bg="white")
canvas.pack(pady=20)

# Piirretään lähtö- ja maaliviivat
canvas.create_line(50, 50, 50, 150, fill="black", width=5)  # Lähtöviiva
canvas.create_line(550, 50, 550, 150, fill="black", width=5)  # Maaliviiva

# Piirretään juoksijat
ernesti_shape = canvas.create_oval(30, 90, 70, 130, fill="blue")  # Ernesti
kernesti_shape = canvas.create_oval(30, 140, 70, 180, fill="red")  # Kernesti

def reset_positions():
    canvas.coords(ernesti_shape, 30, 90, 70, 130)  
    canvas.coords(kernesti_shape, 30, 140, 70, 180)  
    root.update()

def run_simulation(name, speed, shape, frequency, duration, aikakerroin):
    progress = 0
    step = 500 / speed  # Mitä nopeampi, sitä suurempi askel (500 on viivan pituus)
    
    start_time = time.time()  # Start time for the runner
    
    while progress < 500:
        progress += step
        canvas.move(shape, step, 0)  # Liikutetaan juoksijaa x-akselilla
        root.update()
        
        # Soitetaan ääni jokaisella askeleella
        winsound.Beep(frequency, duration)
        
        time.sleep(aikakerroin)  # Simulaatio sekunnin välein tai nopeammin
    
    # Kun juoksija on ylittänyt maaliviivan, resetoi paikat
    reset_positions()

    end_time = time.time()  
    total_time = end_time - start_time  
    show_result(name, total_time)
    return total_time

def show_result(name, time_taken):
    result_label.config(text=f"{name} juoksi 100m aikaan {time_taken:.2f} sekuntia!")
    root.update()

# Yhteislähtö-funktio
def yhteis_laukaisu():
    reset_positions()  
    ernesti_thread = threading.Thread(target=juokse_ernesti)
    kernesti_thread = threading.Thread(target=juokse_kernesti)
    ernesti_thread.start()
    kernesti_thread.start()

def juokse_ernesti():
    return run_simulation("Ernesti", kehitys["Ernesti"], ernesti_shape, 100, 100, 1)

def juokse_kernesti():
    return run_simulation("Kernesti", kehitys["Kernesti"], kernesti_shape, 1100, 50, 1)

def harjoittele_1_paiva(name, shape):
    aikakerroin = 1 / 1000  # Vähennetään sekuntia
    harjoitukset = 10  # Esim. 10 kertaa 100m päivän aikana
    for _ in range(harjoitukset):
        reset_positions()  
        run_simulation(name, kehitys[name], shape, 100, 100, aikakerroin)

def harjoittele_1_kuukausi(name, shape):
    aikakerroin = 1 / 1000
    harjoitukset = 30 * 10  # 30 päivää kuukaudessa, 10 harjoitusta per päivä
    for _ in range(harjoitukset):
        reset_positions()  #
        run_simulation(name, kehitys[name], shape, 100, 100, aikakerroin)
        kehitys[name] -= 0.01  # Esimerkkinä kehityksen lasku

def harjoittele_1_vuosi(name, shape):
    aikakerroin = 1 / 1000
    harjoitukset = 365 * 10  # 365 päivää vuodessa
    for _ in range(harjoitukset):
        reset_positions()  
        run_simulation(name, kehitys[name], shape, 100, 100, aikakerroin)
        kehitys[name] -= 0.01  # Kehityksen päivitys

# Käyttöliittymän komponentit
ernesti_button = tk.Button(root, text="Juokse Ernesti!", command=lambda: threading.Thread(target=juokse_ernesti).start())
ernesti_button.pack(pady=10)

kernesti_button = tk.Button(root, text="Juokse Kernesti!", command=lambda: threading.Thread(target=juokse_kernesti).start())
kernesti_button.pack(pady=10)

# Yhteislähtöpainike
yhteis_laukaisu_button = tk.Button(root, text="Yhteis Laukaisu!", command=lambda: threading.Thread(target=yhteis_laukaisu).start())
yhteis_laukaisu_button.pack(pady=10)

# Napit harjoittelulle
harjoittele_paiva_button = tk.Button(root, text="Harjoittele 1 päivä - Ernesti", command=lambda: threading.Thread(target=harjoittele_1_paiva, args=("Ernesti", ernesti_shape)).start())
harjoittele_paiva_button.pack(pady=10)

harjoittele_kuukausi_button = tk.Button(root, text="Harjoittele 1 kuukausi - Ernesti", command=lambda: threading.Thread(target=harjoittele_1_kuukausi, args=("Ernesti", ernesti_shape)).start())
harjoittele_kuukausi_button.pack(pady=10)

harjoittele_vuosi_button = tk.Button(root, text="Harjoittele 1 vuosi - Ernesti", command=lambda: threading.Thread(target=harjoittele_1_vuosi, args=("Ernesti", ernesti_shape)).start())
harjoittele_vuosi_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
