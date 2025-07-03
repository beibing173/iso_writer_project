# 专业ISO写入器 v2.0

一个功能强大的可引导USB创建工具，支持自动集成PE工具系统。

## 🚀 主要特性

- **智能ISO写入**: 支持各种ISO文件格式的写入
- **自动PE集成**: 自动检测并集成同目录下的pe.iso文件
- **多重引导支持**: 支持UEFI和Legacy引导模式
- **智能设备检测**: 自动扫描和识别USB设备
- **数据完整性验证**: 写入后自动验证数据完整性
- **跨平台支持**: 支持Windows、Linux和macOS
- **精美界面**: 现代化的图形用户界面
- **进度显示**: 实时显示写入进度和状态

## 📋 系统要求

### Windows
- Windows 7 或更高版本
- 管理员权限
- 至少1GB可用内存

### Linux
- Ubuntu 18.04 或更高版本（其他发行版类似）
- sudo权限
- 已安装parted、syslinux等工具

### macOS
- macOS 10.12 或更高版本
- 管理员权限

## 📦 安装说明

### 方式一：使用预编译版本（推荐）
1. 下载发布包中的`ISO写入器.exe`文件
2. 将`pe.iso`文件放在与exe文件相同的目录中
3. 以管理员身份运行exe文件

### 方式二：从源码运行
1. 确保已安装Python 3.7或更高版本
2. 安装依赖包：
   ```bash
   pip install tkinter
   ```
3. 运行程序：
   ```bash
   python iso_writer_final.py
   ```

## 🔧 打包说明

如果您想自己打包程序，请按照以下步骤：

### 准备工作
1. 确保所有源文件在同一目录中：
   - `iso_writer_final.py` - 主程序文件
   - `build_exe.py` - 打包脚本
   - `pe.iso` - PE工具文件（必需）

### 自动打包
1. 运行打包脚本：
   ```bash
   python build_exe.py
   ```
2. 脚本会自动：
   - 检查并安装PyInstaller
   - 创建打包配置
   - 构建可执行文件
   - 生成最终的exe文件

### 手动打包
如果自动打包失败，可以手动执行：

1. 安装PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 创建规格文件`iso_writer.spec`：
   ```python
   # -*- mode: python ; coding: utf-8 -*-
   
   a = Analysis(
       ['iso_writer_final.py'],
       pathex=[],
       binaries=[],
       datas=[('pe.iso', '.')],
       hiddenimports=[],
       hookspath=[],
       runtime_hooks=[],
       excludes=[],
       win_no_prefer_redirects=False,
       win_private_assemblies=False,
       cipher=None,
       noarchive=False,
   )
   
   pyz = PYZ(a.pure, a.zipped_data, cipher=None)
   
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
       console=False,
       icon='icon.ico'
   )
   ```

3. 执行打包：
   ```bash
   pyinstaller --clean iso_writer.spec
   ```

4. 打包完成后，可执行文件位于`dist`目录中。

## 📖 使用指南

### 基本使用流程

1. **启动程序**
   - 以管理员身份运行程序
   - 程序会自动检测pe.iso文件状态

2. **选择ISO文件**
   - 点击"浏览"按钮选择要写入的ISO文件
   - 支持所有标准ISO格式

3. **选择目标设备**
   - 点击"扫描"按钮自动检测USB设备
   - 或手动输入设备路径

4. **配置选项**
   - **写入后验证**: 确保数据完整性（推荐开启）
   - **格式化USB**: 清除设备上的所有数据（推荐开启）
   - **创建可引导USB**: 安装引导程序（推荐开启）

5. **开始制作**
   - 点击"开始制作"按钮
   - 确认警告对话框
   - 等待制作完成

### 设备路径格式

不同操作系统的设备路径格式：

- **Windows**: `D:` 或 `E:` （盘符，不含反斜杠）
- **Linux**: `/dev/sdb` 或 `/dev/sdc` （完整设备路径）
- **macOS**: `/dev/disk2` 或 `/dev/disk3` （完整设备路径）

### PE工具集成

程序会自动检测并集成同目录下的`pe.iso`文件：

- ✅ **找到pe.iso**: 程序会自动集成PE工具到USB设备
- ❌ **未找到pe.iso**: 程序仍可正常工作，但不会集成PE工具

## ⚠️ 重要提醒

### 数据安全
- **写入操作会完全擦除USB设备上的所有数据**
- 请在操作前备份重要数据
- 确认选择了正确的目标设备

### 权限要求
- **Windows**: 必须以管理员身份运行
- **Linux**: 需要sudo权限
- **macOS**: 需要管理员权限

### 设备要求
- USB设备容量应大于ISO文件大小
- 建议使用USB 3.0或更高版本以获得更好性能
- 确保USB设备工作正常

## 🔍 故障排除

### 常见问题

**Q: 程序提示"需要管理员权限"**
A: 请右键点击程序，选择"以管理员身份运行"

**Q: 找不到USB设备**
A: 
- 确保USB设备已正确连接
- 尝试重新插拔USB设备
- 检查设备是否被其他程序占用

**Q: 写入失败**
A:
- 检查ISO文件是否完整
- 确保USB设备有足够空间
- 尝试使用其他USB设备

**Q: 无法启动制作的USB**
A:
- 确保在BIOS中启用了USB启动
- 检查BIOS启动模式（UEFI/Legacy）
- 尝试在不同电脑上测试

**Q: PE工具未集成**
A:
- 确保pe.iso文件与程序在同一目录
- 检查pe.iso文件是否完整
- 重新下载或获取pe.iso文件

### 错误代码

- **错误001**: ISO文件不存在或无法访问
- **错误002**: USB设备路径无效
- **错误003**: 权限不足
- **错误004**: 设备空间不足
- **错误005**: 写入过程中断

### 获取帮助

如果遇到其他问题：

1. 查看程序内置的帮助文档
2. 检查系统日志获取详细错误信息
3. 确保使用最新版本的程序

## 📝 更新日志

### v2.0 (当前版本)
- ✨ 全新的现代化界面设计
- 🔧 自动PE工具集成功能
- 🚀 智能USB设备检测
- ✅ 增强的数据验证机制
- 🌐 改进的跨平台兼容性
- 📊 实时进度显示
- 🛡️ 增强的错误处理

### v1.0
- 🎯 基础ISO写入功能
- 💾 简单的设备选择
- ⚙️ 基本的引导支持

## 📄 许可证

本程序遵循MIT许可证，详情请参阅LICENSE文件。

## 🤝 贡献

欢迎提交问题报告和功能建议！

---

**注意**: 使用本程序时请遵守相关法律法规，作者不对因使用本程序造成的任何损失承担责任。

