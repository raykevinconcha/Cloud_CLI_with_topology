# Generar lista de números entre 5901 y 5950
vnc_wk1_numbers = list(range(5901, 5951))

# Guardar la lista en un archivo
with open("../vnc_wk1.txt", "w") as file:
    for number in vnc_wk1_numbers:
        file.write(str(number) + "\n")

# Generar lista de números entre 5951 y 6000
vnc_wk2_numbers = list(range(5951, 6001))

# Guardar la lista en un archivo
with open("../vnc_wk2.txt", "w") as file:
    for number in vnc_wk2_numbers:
        file.write(str(number) + "\n")

# Generar lista de números entre 6001 y 6050
vnc_wk3_numbers = list(range(6001, 6051))

# Guardar la lista en un archivo
with open("../vnc_wk3.txt", "w") as file:
    for number in vnc_wk3_numbers:
        file.write(str(number) + "\n")
