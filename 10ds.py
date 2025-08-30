# -------------------------------
# Disk Scheduling Algorithms
# FCFS, SCAN, C-SCAN
# -------------------------------

def fcfs(requests, head):
    print("\n--- FCFS Disk Scheduling ---")
    total_movement = 0
    cur_pos = head
    for req in requests:
        movement = abs(req - cur_pos)
        print(f"Move from {cur_pos} to {req} -> movement = {movement}")
        total_movement += movement
        cur_pos = req
    print(f"Total head movement (FCFS): {total_movement}\n")


def scan(requests, head, disk_size, direction='up'):
    print("\n--- SCAN Disk Scheduling ---")
    total_movement = 0
    cur_pos = head
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'up':
        for req in right:
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req
        # Go to end of disk if not already there
        if cur_pos != disk_size - 1:
            movement = abs(cur_pos - (disk_size - 1))
            print(f"Move to end {disk_size - 1} -> movement = {movement}")
            total_movement += movement
            cur_pos = disk_size - 1
        for req in reversed(left):
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req
    else:  # direction 'down'
        for req in reversed(left):
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req
        if cur_pos != 0:
            movement = cur_pos
            print(f"Move to start 0 -> movement = {movement}")
            total_movement += movement
            cur_pos = 0
        for req in right:
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req

    print(f"Total head movement (SCAN): {total_movement}\n")


def c_scan(requests, head, disk_size, direction='up'):
    print("\n--- C-SCAN Disk Scheduling ---")
    total_movement = 0
    cur_pos = head
    requests = sorted(requests)
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'up':
        # Move towards the end
        for req in right:
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req
        # Jump to beginning without servicing requests
        if left:
            movement = abs(cur_pos - (disk_size - 1))
            total_movement += movement
            cur_pos = 0
            print(f"Jump to start 0 (C-SCAN) -> movement = {movement}")
            for req in left:
                movement = abs(cur_pos - req)
                print(f"Move from {cur_pos} to {req} -> movement = {movement}")
                total_movement += movement
                cur_pos = req
    else:  # direction 'down'
        for req in reversed(left):
            movement = abs(cur_pos - req)
            print(f"Move from {cur_pos} to {req} -> movement = {movement}")
            total_movement += movement
            cur_pos = req
        if right:
            movement = abs(cur_pos - 0)
            total_movement += movement
            cur_pos = disk_size - 1
            print(f"Jump to end {disk_size - 1} (C-SCAN) -> movement = {movement}")
            for req in reversed(right):
                movement = abs(cur_pos - req)
                print(f"Move from {cur_pos} to {req} -> movement = {movement}")
                total_movement += movement
                cur_pos = req

    print(f"Total head movement (C-SCAN): {total_movement}\n")


# -------------------------------
# Driver Code
# -------------------------------
if __name__ == "__main__":
    disk_size = 200  # 0 to 199
    head = 50
    requests = [82, 170, 43, 140, 24, 16, 190]

    print(f"Initial Head Position: {head}")
    print(f"Request Queue: {requests}")

    fcfs(requests, head)
    scan(requests, head, disk_size, direction='up')
    c_scan(requests, head, disk_size, direction='up')
