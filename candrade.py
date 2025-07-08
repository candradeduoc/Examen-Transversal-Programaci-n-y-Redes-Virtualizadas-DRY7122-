

vlan = int(input("Ingrese el número de la VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} corresponde a una VLAN del rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} corresponde a una VLAN del rango EXTENDIDO.")
else:
    print("Número de VLAN inválido. Debe estar entre 1 y 4094.")
