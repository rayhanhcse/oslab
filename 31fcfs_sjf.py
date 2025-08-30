def fcfs(processes, burst_time):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Waiting time calculation
    for i in range(1, n):
        waiting_time[i] = waiting_time[i-1] + burst_time[i-1]

    # Turnaround time = waiting + burst
    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    # Averages
    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    print("\n=== FCFS Scheduling ===")
    print("Process\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


def sjf(processes, burst_time):
    n = len(processes)

    # Sort by burst time
    sorted_processes = sorted(zip(processes, burst_time), key=lambda x: x[1])
    processes, burst_time = zip(*sorted_processes)

    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Waiting time calculation
    for i in range(1, n):
        waiting_time[i] = waiting_time[i-1] + burst_time[i-1]

    # Turnaround time = waiting + burst
    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    # Averages
    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    print("\n=== SJF Scheduling ===")
    print("Process\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


if __name__ == "__main__":
    # Input processes and burst times
    n = int(input("Enter number of processes: "))
    processes = []
    burst_time = []

    for i in range(n):
        processes.append(i + 1)
        bt = int(input(f"Enter Burst Time for Process P{i+1}: "))
        burst_time.append(bt)

    # Call both algorithms
    fcfs(processes, burst_time)
    sjf(processes, burst_time)
