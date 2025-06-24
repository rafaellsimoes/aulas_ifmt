import psutil
pid = 29348 # substitua por um PID válido
if psutil.pid_exists(pid):
    p = psutil.Process(pid)
    print(f"Nome  {p.name()}")
    print(f"Executável {p.exe()}")
    print(f"Diretório {p.cwd()}")
    print(f"Status {p.status()}")
    print(f"Uso de CPU {p.cpu_percent()}%")
    print(f"Uso de memória {p.memory_info().rss / 1024 / 1024:.2f} MB")
