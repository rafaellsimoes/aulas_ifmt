import psutil
# Uso da CPU
print(f"Uso da CPU: {psutil.cpu_percent(interval=1)}%")

# Uso de memória
mem = psutil.virtual_memory()
print(f"Memória total: {mem.total / 1024 / 1024:.2f} MB")
print(f"Memória usada: {mem.used / 1024 / 1024:.2f} MB")
print(f"Memória livre: {mem.available / 1024 / 1024:.2f} MB")
