#!/usr/bin/env python3
"""
ISO写入器打包脚本
使用PyInstaller将Python程序打包成独立的exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['iso_writer_final.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('pe.iso', '.'),  # 将pe.iso文件包含到打包中
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ISO写入器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # 如果有图标文件
)
'''
    
    with open('iso_writer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ 已创建PyInstaller规格文件")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    try:
        # 使用规格文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "iso_writer.spec"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 构建成功！")
            return True
        else:
            print(f"❌ 构建失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中出错: {e}")
        return False

def create_icon():
    """创建简单的图标文件（如果不存在）"""
    if not os.path.exists('icon.ico'):
        print("ℹ️ 未找到icon.ico文件，将使用默认图标")
        # 这里可以创建一个简单的图标或者跳过
        return False
    return True

def copy_pe_file():
    """确保pe.iso文件存在"""
    if not os.path.exists('pe.iso'):
        print("⚠️ 警告: 未找到pe.iso文件")
        print("请将pe.iso文件放在与脚本相同的目录中")
        
        # 创建一个空的pe.iso文件作为占位符
        with open('pe.iso', 'wb') as f:
            f.write(b'')
        print("已创建空的pe.iso占位符文件")
        return False
    else:
        pe_size = os.path.getsize('pe.iso') / (1024 * 1024)
        print(f"✅ 找到pe.iso文件 ({pe_size:.1f} MB)")
        return True

def create_batch_file():
    """创建批处理文件用于快速构建"""
    batch_content = '''@echo off
echo 正在构建ISO写入器...
python build_exe.py
pause
'''
    
    with open('build.bat', 'w', encoding='gbk') as f:
        f.write(batch_content)
    
    print("✅ 已创建build.bat批处理文件")

def cleanup_build_files():
    """清理构建过程中的临时文件"""
    cleanup_dirs = ['build', '__pycache__']
    cleanup_files = ['iso_writer.spec']
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name, ignore_errors=True)
            print(f"🧹 已清理目录: {dir_name}")
    
    for file_name in cleanup_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🧹 已清理文件: {file_name}")

def main():
    """主函数"""
    print("=" * 50)
    print("ISO写入器 - 自动打包脚本")
    print("=" * 50)
    
    # 检查必要文件
    if not os.path.exists('iso_writer_final.py'):
        print("❌ 错误: 未找到iso_writer_final.py文件")
        return False
    
    # 检查并安装PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # 准备文件
    copy_pe_file()
    create_icon()
    
    # 创建规格文件
    create_spec_file()
    
    # 构建可执行文件
    if build_executable():
        print("\n" + "=" * 50)
        print("🎉 打包完成！")
        print("=" * 50)
        print("可执行文件位置: dist/ISO写入器.exe")
        print("文件大小:", end=" ")
        
        exe_path = "dist/ISO写入器.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"{size_mb:.1f} MB")
        else:
            print("未知")
        
        print("\n使用说明:")
        print("1. 将pe.iso文件与exe文件放在同一目录")
        print("2. 以管理员身份运行exe文件")
        print("3. 选择ISO文件和目标USB设备")
        print("4. 点击开始制作")
        
        # 创建批处理文件
        create_batch_file()
        
        return True
    else:
        print("\n❌ 打包失败！")
        return False

if __name__ == "__main__":
    try:
        success = main()
        
        # 询问是否清理临时文件
        if success:
            response = input("\n是否清理构建过程中的临时文件？(y/n): ")
            if response.lower() in ['y', 'yes', '是']:
                cleanup_build_files()
        
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    
    input("\n按回车键退出...")

