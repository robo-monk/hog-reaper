#!/usr/bin/env python3

import subprocess

# Define color codes
color_red = '\033[0;31m'
color_green = '\033[0;32m'
color_yellow = '\033[0;33m'
color_blue = '\033[0;34m'
color_magenta = '\033[0;35m'
color_cyan = '\033[0;36m'
color_reset = '\033[0m'

# Get the top 10 most CPU-intensive processes and their information
output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
top_processes = sorted(output.split('\n')[1:-1], key=lambda x: float(x.split()[2]), reverse=True)[:10]

# Format the output of top processes
top_processes_formatted = []
for process in top_processes:
    pid, user, cpu, mem, vsz, rss, tty, stat, start, time, *command_parts = process.split(None, 10)
    command = ' '.join(command_parts)
    if len(command_parts) > 1:
        file_path = command_parts[1]
    else:
        file_path = ''
    top_processes_formatted.append(f"{pid:<8}{user:<8}{cpu:<8}{mem:<8}{time:<15}{command.split()[0]:<15}{file_path}")

# Output the list of top processes with colors
print("Top 10 CPU-intensive processes:")
print(f"{color_yellow}PID      USER     CPU      MEM      TIME            COMMAND         FILE{color_reset}")
for i, process in enumerate(top_processes_formatted):
    if i % 2 == 0:
        print(f"\033[0;37m{process}\033[0;31m")
    else:
        print(f"\033[0;37m{process}\033[0;35m")

# Reset colors
print(color_reset)

# Suggest processes to kill based on their memory and CPU usage
print("Suggested processes to kill:")
output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
for process in output.split('\n')[1:-1]:
    pid, user, cpu, mem, vsz, rss, tty, stat, start, time, *command_parts = process.split(None, 10)
    command = ' '.join(command_parts)
    if len(command_parts) > 1:
        file_path = command_parts[1]
    else:
        file_path = ''
    if float(cpu) > 70 or float(mem) > 70:
        if user != "root" and not user.startswith("_"):
            print(f"{pid:<8}{user:<8}{cpu:<8}{mem:<8}{time:<15}{command.split()[0]:<15}{file_path}")

