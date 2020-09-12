from utils.key_gen import key_gen
import wmi

class Register():
    @staticmethod
    def get_register_info():
        c = wmi.WMI()
        first_disk_serial_no = c.Win32_DiskDrive()[0].SerialNumber
        first_process_id = c.Win32_Processor()[0].ProcessorId.strip()
        info = key_gen.get_key(first_disk_serial_no, first_process_id)
        return info
