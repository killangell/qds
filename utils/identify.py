import wmi

c = wmi.WMI()

first_disk_serial_no = c.Win32_DiskDrive()[0].SerialNumber
# base_board_serial_no = c.Win32_BaseBoard()[0].SerialNumber
first_process_id = c.Win32_Processor()[0].ProcessorId.strip()

print("disk: {0}".format(first_disk_serial_no))
# print("board: {0}".format(base_board_serial_no))
print("cpu: {0}".format(first_process_id))