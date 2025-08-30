def round_robin(processes, burst_time, arrival_time, quantum):
    n = len(processes)
    remaining_time = burst_time.copy()
    waiting_time = [0] * n
    turnaround_time = [0] * n
    t = 0  # current time
    ready_queue = []
    completed = [False] * n

    print("\n=== Round Robin Scheduling ===")
    print(f"Time Quantum = {quantum}\n")

    # Keep looping until all processes are done
    while True:
        done = True
        for i in range(n):
            if remaining_time[i] > 0:
                done = False

                if remaining_time[i] > quantum:
                    t += quantum
                    remaining_time[i] -= quantum
                else:
                    t += remaining_time[i]
                    waiting_time[i] = t - burst_time[i] - arrival_time[i]
                    if waiting_time[i] < 0:
                        waiting_time[i] = 0
                    remaining_time[i] = 0

        if done:
            break

    # Turnaround time
    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    avg_wt = sum(waiting_time) / n
    avg_tat = sum(turnaround_time) / n

    print("Process\tArrival\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"P{processes[i]}\t{arrival_time[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")

    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


if __name__ == "__main__":
    n = int(input("Enter number of processes: "))
    processes = []
    burst_time = []
    arrival_time = []

    for i in range(n):
        processes.append(i + 1)
        at = int(input(f"Enter Arrival Time for Process P{i+1}: "))
        bt = int(input(f"Enter Burst Time for Process P{i+1}: "))
        arrival_time.append(at)
        burst_time.append(bt)

    quantum = int(input("Enter Time Quantum: "))

    round_robin(processes, burst_time, arrival_time, quantum)
