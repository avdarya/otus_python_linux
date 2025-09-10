import subprocess
from collections import defaultdict


def run_command(*args):
    result = subprocess.run(args, stdout=subprocess.PIPE, text=True)
    return result.stdout

def get_ps_aux_lines():
    output = run_command('ps', 'aux')
    return output.strip().split('\n')[1:]

def get_users(lines):
    users = set()
    for line in lines:
        parts = line.split(None, 10)
        users.add(parts[0])
    return users

def get_process_count(lines):
    return len(lines)

def get_users_processes(lines):
    counts = defaultdict(int)
    for line in lines:
        user = line.split(None, 10)[0]
        counts[user] += 1
    return counts

def get_total_mem(lines):
    total_mem = 0.0
    for line in lines:
        parts = line.split(None, 10)
        if len(parts) >= 4:
            try:
                mem = float(parts[3])
                total_mem += mem
            except ValueError:
                continue
    return round(total_mem, 1)

def get_total_cpu(lines):
    total_cpu = 0.0
    for line in lines:
        parts = line.split(None, 10)
        if len(parts) >= 3:
            try:
                cpu = float(parts[2])
                total_cpu += cpu
            except ValueError:
                continue
    return round(total_cpu, 1)

def get_top_mem_proc(lines):
    max_mem = -1.0
    top_proc_mem = ""
    for line in lines:
        parts = line.split(None, 10)
        if len(parts) >= 4:
            try:
                mem = float(parts[3])
                if mem > max_mem:
                    max_mem = mem
                    top_proc_mem = parts[10][:20]
            except ValueError:
                continue
    return round(max_mem, 1), top_proc_mem

def get_top_cpu_proc(lines):
    max_cpu = -1.0
    top_proc_cpu = ''
    for line in lines:
        parts = line.split(None, 10)
        if len(parts) >= 3:
            try:
                cpu = float(parts[2])
                if cpu > max_cpu:
                    max_cpu = cpu
                    top_proc_cpu = parts[10][:20]
            except ValueError:
                continue
    return round(max_cpu, 1), top_proc_cpu

def save_report_to_file(report):
    filename = "scan.txt"
    with open(filename, 'w') as f:
        f.write(report)

def generate_report():
    lines = get_ps_aux_lines()
    users = get_users(lines)
    process_count = get_process_count(lines)
    users_processes = get_users_processes(lines)
    total_mem = get_total_mem(lines)
    total_cpu = get_total_cpu(lines)
    max_mem, top_proc_mem = get_top_mem_proc(lines)
    max_cpu, top_proc_cpu = get_top_cpu_proc(lines)

    report = []
    report.append("=" * 60)
    report.append("Запуск парсера процессов")
    report.append("=" * 60)
    report.append("Отчёт о состоянии системы:")
    report.append("Пользователи системы: " + ", ".join(f"\'{u}\'" for u in users))
    report.append(f'Процессов запущено: {process_count}')
    report.append("\n")
    report.append("Пользовательских процессов:")
    for k, v in users_processes.items():
        report.append(f"{k}: {v}")
    report.append("\n")
    report.append(f"Всего памяти используется: {total_mem}%")
    report.append(f"Всего CPU используется: {total_cpu}%")
    report.append(f"Больше всего памяти использует: {max_mem}% {top_proc_mem}")
    report.append(f"Больше всего CPU использует: {max_cpu}% {top_proc_cpu}")
    report.append("=" * 60)
    report.append("Запуск парсера завершен")
    report.append("=" * 60)

    return '\n'.join(report)

def main():
    report = generate_report()
    print(report)
    save_report_to_file(report)


if __name__ == "__main__":
    main()
