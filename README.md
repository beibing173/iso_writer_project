ISO写入器项目文件结构
========================

📁 项目根目录/
├── 📄 iso_writer_final.py      # 主程序文件（核心）
├── 📄 build_exe.py             # 自动打包脚本
├── 📄 bootloader_utils.py      # 引导工具模块（可选）
├── 📄 pe.iso                   # PE工具文件（必需）
├── 📄 requirements.txt         # Python依赖列表
├── 📄 README.md               # 项目说明文档
├── 📄 打包教程.md              # 详细打包教程
├── 📄 todo.md                 # 开发任务清单
└── 📄 项目结构.txt             # 本文件

核心文件说明：
=============

🔥 iso_writer_final.py
   - 主程序文件，包含完整的GUI界面和ISO写入功能
   - 自动检测并集成同目录下的pe.iso文件
   - 支持Windows、Linux、macOS跨平台运行
   - 具有现代化的图形用户界面

🔧 build_exe.py
   - 自动化打包脚本
   - 自动检测并安装PyInstaller
   - 创建打包配置文件
   - 一键生成可执行文件

💾 pe.iso
   - PE工具系统文件
   - 程序会自动检测此文件并集成到USB中
   - 如果文件不存在，程序仍可正常工作但不会集成PE功能

📋 requirements.txt
   - 列出了所有Python依赖包
   - 用于pip安装依赖：pip install -r requirements.txt

📖 README.md
   - 完整的项目说明文档
   - 包含安装、使用、故障排除等信息

📚 打包教程.md
   - 详细的打包指南
   - 包含自动和手动打包方法
   - 故障排除和优化建议

使用流程：
=========

1. 开发阶段：
   python iso_writer_final.py

2. 打包阶段：
   python build_exe.py

3. 分发阶段：
   将dist/ISO写入器.exe和pe.iso一起分发

最小分发包：
===========
📁 ISO写入器_v2.0/
├── 📄 ISO写入器.exe    # 主程序（必需）
├── 📄 pe.iso          # PE工具（推荐）
└── 📄 README.md       # 使用说明（推荐）

注意事项：
=========
- pe.iso文件必须与exe文件在同一目录
- 程序需要管理员权限运行
- 支持的ISO文件格式：标准ISO 9660格式
- 推荐USB设备：USB 3.0或更高版本

# ISO写入器依赖包列表

# 核心依赖
# tkinter - GUI界面库（Python标准库，通常无需单独安装）

# 打包依赖
pyinstaller>=5.0.0

# 可选依赖（用于增强功能）
# 注意：以下包在某些系统上可能需要额外的系统依赖

# Windows特定依赖
pywin32>=300; sys_platform == "win32"

# 跨平台文件操作
pathlib2>=2.3.0; python_version < "3.4"

# 进度条和界面增强
tqdm>=4.60.0

# 系统信息获取
psutil>=5.8.0

# 注意事项：
# 1. tkinter是Python标准库的一部分，在大多数Python安装中都包含
# 2. 如果在Linux上tkinter不可用，请安装：
#    Ubuntu/Debian: sudo apt-get install python3-tk
#    CentOS/RHEL: sudo yum install tkinter
#    Fedora: sudo dnf install python3-tkinter
# 3. 在macOS上，tkinter通常随Python一起安装
# 4. pywin32仅在Windows上需要，用于系统级操作
# 5. 其他依赖包是可选的，用于增强功能

# ISO写入器打包教程

本教程将详细指导您如何将Python源码打包成独立的exe可执行文件。

## 📋 准备工作

### 1. 环境要求
- Python 3.7 或更高版本
- Windows 操作系统（推荐Windows 10）
- 至少2GB可用磁盘空间

### 2. 必需文件
确保以下文件在同一目录中：
```
项目目录/
├── iso_writer_final.py    # 主程序文件
├── build_exe.py          # 自动打包脚本
├── pe.iso                # PE工具文件（重要！）
├── requirements.txt      # 依赖列表
└── README.md            # 说明文档
```

### 3. 检查Python环境
打开命令提示符，检查Python版本：
```bash
python --version
```
应该显示Python 3.7或更高版本。

## 🚀 自动打包（推荐）

### 步骤1：运行自动打包脚本
1. 打开命令提示符（以管理员身份运行）
2. 导航到项目目录：
   ```bash
   cd C:\path\to\your\project
   ```
3. 运行自动打包脚本：
   ```bash
   python build_exe.py
   ```

### 步骤2：等待打包完成
脚本会自动执行以下操作：
- ✅ 检查PyInstaller是否已安装
- 📦 自动安装PyInstaller（如果需要）
- 🔍 检查pe.iso文件
- 📝 创建打包配置文件
- 🔨 构建可执行文件
- 🧹 清理临时文件（可选）

### 步骤3：获取结果
打包成功后，您会在`dist`目录中找到：
```
dist/
└── ISO写入器.exe    # 最终的可执行文件
```

## 🔧 手动打包

如果自动打包失败，可以按照以下步骤手动打包：

### 步骤1：安装PyInstaller
```bash
pip install pyinstaller
```

### 步骤2：创建打包配置
创建文件`iso_writer.spec`：
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['iso_writer_final.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('pe.iso', '.'),  # 重要：包含pe.iso文件
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
    icon='icon.ico',  # 可选：自定义图标
)
```

### 步骤3：执行打包
```bash
pyinstaller --clean iso_writer.spec
```

### 步骤4：测试可执行文件
1. 进入`dist`目录
2. 以管理员身份运行`ISO写入器.exe`
3. 测试所有功能是否正常

## 🎨 自定义打包

### 添加自定义图标
1. 准备一个`.ico`格式的图标文件
2. 将图标文件命名为`icon.ico`并放在项目目录中
3. 重新运行打包脚本

### 修改程序信息
编辑`iso_writer.spec`文件，在`exe`部分添加版本信息：
```python
exe = EXE(
    # ... 其他参数 ...
    version='version_info.txt',  # 版本信息文件
    # ... 其他参数 ...
)
```

创建`version_info.txt`文件：
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'Your Company'),
           StringStruct(u'FileDescription', u'专业ISO写入器'),
           StringStruct(u'FileVersion', u'2.0.0.0'),
           StringStruct(u'InternalName', u'ISO写入器'),
           StringStruct(u'LegalCopyright', u'Copyright (C) 2025'),
           StringStruct(u'OriginalFilename', u'ISO写入器.exe'),
           StringStruct(u'ProductName', u'专业ISO写入器'),
           StringStruct(u'ProductVersion', u'2.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

## 🔍 故障排除

### 常见问题及解决方案

**问题1：PyInstaller安装失败**
```
解决方案：
1. 确保网络连接正常
2. 尝试使用国内镜像：
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
3. 更新pip：python -m pip install --upgrade pip
```

**问题2：打包过程中出现模块缺失错误**
```
解决方案：
1. 安装缺失的模块：pip install 模块名
2. 在spec文件的hiddenimports中添加模块名
3. 检查Python环境是否完整
```

**问题3：exe文件无法运行**
```
解决方案：
1. 检查是否以管理员身份运行
2. 确保pe.iso文件与exe在同一目录
3. 检查Windows Defender是否误报
4. 尝试在其他电脑上测试
```

**问题4：打包文件过大**
```
解决方案：
1. 在spec文件中添加excludes排除不需要的模块
2. 使用upx压缩（已在配置中启用）
3. 移除不必要的依赖包
```

**问题5：pe.iso文件未正确包含**
```
解决方案：
1. 确保pe.iso文件存在于项目目录
2. 检查spec文件中的datas配置
3. 重新运行打包脚本
```

## 📊 打包优化

### 减小文件大小
1. **排除不需要的模块**：
   ```python
   excludes=['matplotlib', 'numpy', 'pandas']  # 示例
   ```

2. **使用UPX压缩**（已启用）：
   ```python
   upx=True
   ```

3. **移除调试信息**：
   ```python
   debug=False
   strip=False
   ```

### 提高启动速度
1. **禁用控制台窗口**：
   ```python
   console=False
   ```

2. **使用单文件模式**（当前配置）：
   所有依赖打包到一个exe文件中

## 📦 分发准备

### 创建安装包
打包完成后，建议创建一个分发包：
```
ISO写入器_v2.0/
├── ISO写入器.exe      # 主程序
├── pe.iso            # PE工具（必需）
├── README.md         # 使用说明
└── 使用教程.txt       # 简化教程
```

### 测试清单
在分发前，请在不同环境中测试：
- ✅ Windows 10 (64位)
- ✅ Windows 11 (64位)
- ✅ 不同的USB设备
- ✅ 不同的ISO文件
- ✅ 管理员权限运行
- ✅ 普通用户权限运行（应该提示需要管理员权限）

## 🎯 最佳实践

1. **版本控制**：为每个版本创建标签
2. **测试充分**：在多种环境中测试
3. **文档完整**：提供详细的使用说明
4. **错误处理**：确保程序有良好的错误提示
5. **用户友好**：界面直观，操作简单

## 📞 技术支持

如果在打包过程中遇到问题：

1. 检查Python和PyInstaller版本兼容性
2. 查看详细的错误日志
3. 确保所有依赖文件都存在
4. 尝试在虚拟环境中打包
5. 参考PyInstaller官方文档

---

**提示**：首次打包可能需要较长时间，请耐心等待。建议在网络良好的环境下进行打包操作。

# ISO写入器使用示例

本文档提供了详细的使用示例，帮助用户快速上手。

## 🎯 快速开始

### 场景1：制作Windows安装盘

**需求**：将Windows 10 ISO制作成可引导USB安装盘

**步骤**：
1. 准备一个8GB或更大的USB设备
2. 下载Windows 10 ISO文件
3. 启动ISO写入器（以管理员身份）
4. 选择Windows 10 ISO文件
5. 选择目标USB设备
6. 确保勾选"创建可引导USB"
7. 点击"开始制作"

**结果**：获得可引导的Windows 10安装USB

### 场景2：制作Linux Live USB

**需求**：制作Ubuntu Live USB用于系统救援

**步骤**：
1. 准备一个4GB或更大的USB设备
2. 下载Ubuntu ISO文件
3. 启动ISO写入器
4. 选择Ubuntu ISO文件
5. 选择目标USB设备
6. 勾选所有推荐选项
7. 开始制作

**结果**：获得Ubuntu Live USB，可用于系统救援

### 场景3：制作集成PE工具的维护盘

**需求**：制作包含PE工具的系统维护盘

**前提条件**：
- 确保pe.iso文件与程序在同一目录
- pe.iso文件包含完整的PE工具系统

**步骤**：
1. 准备一个16GB或更大的USB设备（推荐）
2. 选择任意可引导的ISO文件
3. 程序会自动检测并显示"PE工具已集成"
4. 正常制作流程
5. 制作完成后USB将包含原ISO内容+PE工具

**结果**：获得集成PE工具的多功能维护USB

## 📱 界面操作指南

### 主界面布局
```
┌─────────────────────────────────────┐
│        🚀 专业ISO写入器              │
│     集成PE工具的可引导USB创建专家     │
├─────────────────────────────────────┤
│ ✅ PE工具已集成 (XXX.X MB)          │
├─────────────────────────────────────┤
│ 📁 选择源ISO文件                    │
│ [ISO文件路径____________] [浏览]     │
├─────────────────────────────────────┤
│ 💾 目标USB设备                      │
│ [设备路径______________] [扫描]     │
│ 示例: D: 或 E: (不要包含反斜杠)      │
├─────────────────────────────────────┤
│ ⚙️ 写入选项                         │
│ ☑ 写入后验证  ☑ 格式化USB  ☑ 创建可引导USB │
├─────────────────────────────────────┤
│ 🔧 集成功能                         │
│ • 自动集成PE工具系统                │
│ • 支持UEFI和Legacy引导              │
│ • 智能设备检测                      │
│ • 数据完整性验证                    │
├─────────────────────────────────────┤
│ [进度条_________________________]   │
│ 状态：准备就绪                      │
├─────────────────────────────────────┤
│ [🚀 开始制作] [⏹️ 停止] [❓ 帮助]    │
└─────────────────────────────────────┘
```

### 操作步骤详解

#### 1. 选择ISO文件
- 点击"浏览"按钮
- 在文件对话框中选择ISO文件
- 支持的格式：.iso文件
- 文件大小：建议小于USB设备容量

#### 2. 选择USB设备
**方法一：自动扫描**
- 点击"扫描"按钮
- 从弹出的设备列表中选择
- 程序会显示设备大小和类型

**方法二：手动输入**
- 直接在文本框中输入设备路径
- Windows：D: 或 E:（不含反斜杠）
- Linux：/dev/sdb 或 /dev/sdc
- macOS：/dev/disk2 或 /dev/disk3

#### 3. 配置选项
- **写入后验证**：推荐开启，确保数据完整性
- **格式化USB**：推荐开启，清除设备上的所有数据
- **创建可引导USB**：推荐开启，安装引导程序

#### 4. 开始制作
- 点击"开始制作"按钮
- 确认警告对话框
- 等待制作完成（显示进度和状态）

## 🔍 常见使用场景

### Windows用户

**制作Windows PE维护盘**：
```
ISO文件：Windows PE ISO
USB设备：16GB USB 3.0
选项：全部勾选
用途：系统维护、数据恢复
```

**制作Windows安装盘**：
```
ISO文件：Windows 10/11 ISO
USB设备：8GB+ USB设备
选项：全部勾选
用途：系统安装、重装
```

### Linux用户

**制作Ubuntu Live USB**：
```
ISO文件：ubuntu-22.04-desktop-amd64.iso
USB设备：4GB+ USB设备
选项：全部勾选
用途：系统试用、安装
```

**制作系统救援盘**：
```
ISO文件：SystemRescue ISO
USB设备：2GB+ USB设备
选项：全部勾选
用途：系统救援、数据恢复
```

### 技术人员

**制作多功能维护盘**：
```
ISO文件：任意可引导ISO
PE工具：完整的PE工具包
USB设备：32GB+ 高速USB设备
选项：全部勾选
用途：综合系统维护
```

## ⚠️ 注意事项

### 设备选择
- 确保选择正确的USB设备
- 备份重要数据（写入会擦除所有数据）
- 推荐使用USB 3.0或更高版本

### 权限要求
- Windows：必须以管理员身份运行
- Linux：需要sudo权限
- macOS：需要管理员权限

### 文件要求
- ISO文件必须完整且未损坏
- pe.iso文件应与程序在同一目录
- USB设备容量应大于ISO文件大小

### 兼容性
- 支持UEFI和Legacy引导模式
- 兼容大多数主流ISO格式
- 适用于各种品牌的USB设备

## 🎉 成功标志

制作成功后，您会看到：
- ✅ 进度条显示100%
- ✅ 状态显示"制作完成！USB设备已准备就绪"
- ✅ 弹出成功对话框
- ✅ USB设备可在BIOS中识别为可引导设备

## 🔧 验证方法

### 简单验证
1. 在文件管理器中查看USB设备
2. 确认文件已正确复制
3. 检查设备属性中的可用空间

### 完整验证
1. 重启计算机
2. 进入BIOS/UEFI设置
3. 查看引导设备列表
4. 确认USB设备出现在列表中
5. 尝试从USB设备启动

---

**提示**：首次使用建议先用不重要的ISO文件和USB设备进行测试，熟悉操作流程后再处理重要数据。

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

