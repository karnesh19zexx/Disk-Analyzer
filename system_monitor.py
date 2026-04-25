import psutil
import time

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    io_counters = psutil.disk_io_counters()
    read_bytes = io_counters.read_bytes / (1024 * 1024)
    write_bytes = io_counters.write_bytes / (1024 * 1024)
    
    return {
        'cpu': round(cpu, 2),
        'ram': round(ram, 2),
        'disk': round(disk, 2),
        'read_speed': round(read_bytes, 2),
        'write_speed': round(write_bytes, 2)
    }

def get_extended_metrics():
    metrics = get_system_metrics()
    
    cpu_freq = psutil.cpu_freq()
    metrics['cpu_freq'] = round(cpu_freq.current if cpu_freq else 0, 2)
    
    metrics['cpu_count'] = psutil.cpu_count()
    metrics['total_ram'] = round(psutil.virtual_memory().total / (1024**3), 2)
    metrics['available_ram'] = round(psutil.virtual_memory().available / (1024**3), 2)
    
    return metrics