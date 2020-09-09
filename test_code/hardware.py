import wmi


c = wmi.WMI()

# # 硬盘序列号
print("disk\n")
for physical_disk in c.Win32_DiskDrive():
    print(physical_disk.SerialNumber)

# CPU序列号
print("cpu\n")
for cpu in c.Win32_Processor():
    print(cpu.ProcessorId.strip())

# 主板序列号
print("board_id\n")
for board_id in c.Win32_BaseBoard():
    print(board_id.SerialNumber.strip())

# mac地址
print("mac\n")
for mac in c.Win32_NetworkAdapter():
    print(mac.MACAddress)

# bios序列号
print("bios\n")
for bios_id in c.Win32_BIOS():
    print(bios_id.SerialNumber.strip())