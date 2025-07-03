import os
import subprocess
import shutil
import tempfile
import platform
from pathlib import Path

class BootloaderManager:
    """引导加载器管理类"""
    
    def __init__(self):
        self.system = platform.system()
        self.temp_dir = None
        
    def create_bootable_usb(self, iso_path, usb_device, pe_iso_path=None):
        """创建可引导USB"""
        try:
            # 创建临时工作目录
            self.temp_dir = tempfile.mkdtemp(prefix="iso_writer_")
            
            # 挂载ISO文件
            iso_mount_point = self.mount_iso(iso_path)
            
            # 准备USB设备
            self.prepare_usb_device(usb_device)
            
            # 复制ISO内容到USB
            self.copy_iso_contents(iso_mount_point, usb_device)
            
            # 安装引导加载器
            self.install_bootloader(usb_device, iso_mount_point)
            
            # 如果有PE文件，集成PE工具
            if pe_iso_path and os.path.exists(pe_iso_path):
                self.integrate_pe_tools(pe_iso_path, usb_device)
                
            # 清理
            self.cleanup(iso_mount_point)
            
            return True
            
        except Exception as e:
            print(f"创建可引导USB时出错: {e}")
            if self.temp_dir:
                self.cleanup()
            return False
            
    def mount_iso(self, iso_path):
        """挂载ISO文件"""
        mount_point = os.path.join(self.temp_dir, "iso_mount")
        os.makedirs(mount_point, exist_ok=True)
        
        if self.system == "Linux":
            # Linux下使用loop设备挂载
            cmd = ["sudo", "mount", "-o", "loop", iso_path, mount_point]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"挂载ISO失败: {result.stderr}")
                
        elif self.system == "Windows":
            # Windows下使用PowerShell挂载
            cmd = ["powershell", "-Command", f"Mount-DiskImage -ImagePath '{iso_path}'"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"挂载ISO失败: {result.stderr}")
            # 获取挂载点
            mount_point = self.get_windows_mount_point(iso_path)
            
        elif self.system == "Darwin":  # macOS
            # macOS下使用hdiutil挂载
            cmd = ["hdiutil", "attach", iso_path, "-mountpoint", mount_point]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"挂载ISO失败: {result.stderr}")
                
        return mount_point
        
    def get_windows_mount_point(self, iso_path):
        """获取Windows下的ISO挂载点"""
        cmd = ["powershell", "-Command", 
               f"Get-DiskImage -ImagePath '{iso_path}' | Get-Volume | Select-Object -ExpandProperty DriveLetter"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            drive_letter = result.stdout.strip()
            return f"{drive_letter}:\\"
        else:
            raise Exception("无法获取Windows ISO挂载点")
            
    def prepare_usb_device(self, usb_device):
        """准备USB设备"""
        if self.system == "Linux":
            # 卸载可能已挂载的分区
            self.unmount_device(usb_device)
            
            # 创建新的分区表和分区
            self.create_partition_table(usb_device)
            
        elif self.system == "Windows":
            # Windows下格式化USB设备
            self.format_usb_windows(usb_device)
            
    def unmount_device(self, device):
        """卸载设备的所有分区"""
        try:
            # 获取设备的所有分区
            result = subprocess.run(["lsblk", "-ln", "-o", "NAME", device], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # 跳过设备本身
                    partition = f"/dev/{line.strip()}"
                    subprocess.run(["sudo", "umount", partition], 
                                 capture_output=True, text=True)
        except Exception:
            pass  # 忽略卸载错误
            
    def create_partition_table(self, device):
        """创建分区表"""
        # 创建GPT分区表
        cmd = ["sudo", "parted", device, "--script", "mklabel", "gpt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"创建分区表失败: {result.stderr}")
            
        # 创建EFI系统分区
        cmd = ["sudo", "parted", device, "--script", "mkpart", "primary", "fat32", "1MiB", "100MiB"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"创建EFI分区失败: {result.stderr}")
            
        # 创建主数据分区
        cmd = ["sudo", "parted", device, "--script", "mkpart", "primary", "fat32", "100MiB", "100%"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"创建数据分区失败: {result.stderr}")
            
        # 设置启动标志
        cmd = ["sudo", "parted", device, "--script", "set", "1", "esp", "on"]
        subprocess.run(cmd, capture_output=True, text=True)
        
        # 格式化分区
        efi_partition = f"{device}1"
        data_partition = f"{device}2"
        
        subprocess.run(["sudo", "mkfs.fat", "-F32", efi_partition], 
                      capture_output=True, text=True)
        subprocess.run(["sudo", "mkfs.fat", "-F32", data_partition], 
                      capture_output=True, text=True)
                      
    def format_usb_windows(self, usb_device):
        """Windows下格式化USB设备"""
        # 使用diskpart格式化
        diskpart_script = f"""
select volume {usb_device.replace(':', '')}
clean
create partition primary
active
format fs=fat32 quick
assign
exit
"""
        
        script_file = os.path.join(self.temp_dir, "diskpart_script.txt")
        with open(script_file, 'w') as f:
            f.write(diskpart_script)
            
        cmd = ["diskpart", "/s", script_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"格式化USB失败: {result.stderr}")
            
    def copy_iso_contents(self, iso_mount_point, usb_device):
        """复制ISO内容到USB"""
        if self.system == "Linux":
            usb_mount_point = os.path.join(self.temp_dir, "usb_mount")
            os.makedirs(usb_mount_point, exist_ok=True)
            
            # 挂载USB数据分区
            data_partition = f"{usb_device}2"
            cmd = ["sudo", "mount", data_partition, usb_mount_point]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"挂载USB失败: {result.stderr}")
                
            # 复制文件
            cmd = ["sudo", "cp", "-r", f"{iso_mount_point}/*", usb_mount_point]
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"复制文件失败: {result.stderr}")
                
            # 卸载USB
            subprocess.run(["sudo", "umount", usb_mount_point], 
                          capture_output=True, text=True)
                          
        elif self.system == "Windows":
            # Windows下直接复制
            cmd = ["xcopy", f"{iso_mount_point}\\*", f"{usb_device}\\", "/E", "/H", "/Y"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"复制文件失败: {result.stderr}")
                
    def install_bootloader(self, usb_device, iso_mount_point):
        """安装引导加载器"""
        if self.system == "Linux":
            self.install_grub_linux(usb_device, iso_mount_point)
        elif self.system == "Windows":
            self.install_bootloader_windows(usb_device, iso_mount_point)
            
    def install_grub_linux(self, usb_device, iso_mount_point):
        """Linux下安装GRUB"""
        try:
            # 挂载EFI分区
            efi_mount_point = os.path.join(self.temp_dir, "efi_mount")
            os.makedirs(efi_mount_point, exist_ok=True)
            
            efi_partition = f"{usb_device}1"
            cmd = ["sudo", "mount", efi_partition, efi_mount_point]
            subprocess.run(cmd, capture_output=True, text=True)
            
            # 安装GRUB到EFI分区
            cmd = ["sudo", "grub-install", "--target=x86_64-efi", 
                   f"--efi-directory={efi_mount_point}", 
                   "--bootloader-id=USB_BOOT", "--removable"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 创建GRUB配置
            self.create_grub_config(efi_mount_point, iso_mount_point)
            
            # 卸载EFI分区
            subprocess.run(["sudo", "umount", efi_mount_point], 
                          capture_output=True, text=True)
                          
        except Exception as e:
            print(f"安装GRUB失败: {e}")
            # 尝试使用syslinux作为备选
            self.install_syslinux(usb_device)
            
    def install_syslinux(self, usb_device):
        """安装Syslinux引导加载器"""
        try:
            data_partition = f"{usb_device}2"
            cmd = ["sudo", "syslinux", "-i", data_partition]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 安装MBR
            cmd = ["sudo", "dd", "if=/usr/lib/syslinux/mbr/mbr.bin", f"of={usb_device}", "bs=440", "count=1"]
            subprocess.run(cmd, capture_output=True, text=True)
            
        except Exception as e:
            print(f"安装Syslinux失败: {e}")
            
    def create_grub_config(self, efi_mount_point, iso_mount_point):
        """创建GRUB配置文件"""
        grub_dir = os.path.join(efi_mount_point, "EFI", "BOOT")
        os.makedirs(grub_dir, exist_ok=True)
        
        grub_cfg = os.path.join(grub_dir, "grub.cfg")
        
        config_content = """
set timeout=10
set default=0

menuentry "Boot from USB" {
    search --set=root --file /boot/vmlinuz
    linux /boot/vmlinuz boot=live
    initrd /boot/initrd.img
}

menuentry "Boot from ISO (if available)" {
    search --set=root --file /boot.iso
    loopback loop /boot.iso
    linux (loop)/boot/vmlinuz boot=live iso-scan/filename=/boot.iso
    initrd (loop)/boot/initrd.img
}
"""
        
        with open(grub_cfg, 'w') as f:
            f.write(config_content)
            
    def install_bootloader_windows(self, usb_device, iso_mount_point):
        """Windows下安装引导加载器"""
        # 检查是否有现有的引导文件
        boot_files = ["bootmgr", "boot", "efi"]
        
        for boot_file in boot_files:
            src_path = os.path.join(iso_mount_point, boot_file)
            if os.path.exists(src_path):
                dst_path = os.path.join(usb_device, boot_file)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
                    
    def integrate_pe_tools(self, pe_iso_path, usb_device):
        """集成PE工具"""
        try:
            # 挂载PE ISO
            pe_mount_point = self.mount_iso(pe_iso_path)
            
            # 创建PE目录
            if self.system == "Linux":
                usb_mount_point = os.path.join(self.temp_dir, "usb_mount")
                os.makedirs(usb_mount_point, exist_ok=True)
                
                data_partition = f"{usb_device}2"
                cmd = ["sudo", "mount", data_partition, usb_mount_point]
                subprocess.run(cmd, capture_output=True, text=True)
                
                pe_dir = os.path.join(usb_mount_point, "PE")
                os.makedirs(pe_dir, exist_ok=True)
                
                # 复制PE文件
                cmd = ["sudo", "cp", "-r", f"{pe_mount_point}/*", pe_dir]
                subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                subprocess.run(["sudo", "umount", usb_mount_point], 
                              capture_output=True, text=True)
                              
            elif self.system == "Windows":
                pe_dir = os.path.join(usb_device, "PE")
                os.makedirs(pe_dir, exist_ok=True)
                
                cmd = ["xcopy", f"{pe_mount_point}\\*", f"{pe_dir}\\", "/E", "/H", "/Y"]
                subprocess.run(cmd, capture_output=True, text=True)
                
            # 卸载PE ISO
            self.cleanup(pe_mount_point)
            
        except Exception as e:
            print(f"集成PE工具失败: {e}")
            
    def cleanup(self, mount_point=None):
        """清理临时文件和挂载点"""
        if mount_point:
            if self.system == "Linux":
                subprocess.run(["sudo", "umount", mount_point], 
                              capture_output=True, text=True)
            elif self.system == "Windows":
                # Windows下卸载ISO
                cmd = ["powershell", "-Command", f"Dismount-DiskImage -ImagePath '{mount_point}'"]
                subprocess.run(cmd, capture_output=True, text=True)
            elif self.system == "Darwin":
                subprocess.run(["hdiutil", "detach", mount_point], 
                              capture_output=True, text=True)
                              
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            
    def verify_bootable_usb(self, usb_device):
        """验证USB是否可引导"""
        try:
            if self.system == "Linux":
                # 检查分区表和引导标志
                result = subprocess.run(["sudo", "parted", usb_device, "print"], 
                                      capture_output=True, text=True)
                return "esp" in result.stdout.lower() or "boot" in result.stdout.lower()
                
            elif self.system == "Windows":
                # 检查引导文件是否存在
                boot_files = ["bootmgr", "boot\\bcd", "efi\\boot\\bootx64.efi"]
                for boot_file in boot_files:
                    if os.path.exists(os.path.join(usb_device, boot_file)):
                        return True
                return False
                
        except Exception:
            return False
            
        return True

