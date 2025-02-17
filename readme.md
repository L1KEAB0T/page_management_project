# 页面管理模拟器

## 概述

页面管理模拟器是一个使用PyQt5开发的桌面应用程序，用于模拟计算机操作系统中的页面置换算法（FIFO和LRU）。用户可以配置总指令数，选择页面置换算法，并通过单步执行或连续执行来观察页面置换的过程和结果。

## 功能特点

- 支持两种页面置换算法：FIFO（先进先出）和LRU（最近最少使用）。
- 用户可以配置总指令数（范围1到320）。
- 实时显示内存块状态和指令执行日志。
- 统计缺页次数和缺页率。

## 目录结构

```
PageManagementSimulator/
│
├── page_management_project.py  # 主程序文件
└── README.md                   # 使用说明文档
```

## 环境依赖

- Python 3.x
- PyQt5

## 安装与运行

### 安装Python

请确保系统已经安装了Python 3.x。可以在终端或命令提示符中运行以下命令检查是否已安装：

```bash
python --version
```

### 安装PyQt5

在终端或命令提示符中运行以下命令安装PyQt5：

```bash
pip install PyQt5
```

### 运行程序

下载或克隆项目到本地，然后在终端或命令提示符中进入项目目录并运行：

```bash
python page_management_project.py
```

## 使用说明

1. **配置指令数和页面置换算法**
   - 启动程序后，可以在界面顶部配置总指令数（范围1到320）和选择页面置换算法（FIFO或LRU）。
   
2. **查看内存状态**
   - 程序界面中部展示了内存块的状态，每个内存块可以显示最多10条指令。

3. **执行指令**
   - 点击“单步执行”按钮可以逐条执行指令。
   - 点击“连续执行”按钮可以一次性执行所有指令。

4. **重置模拟**
   - 点击“重置”按钮可以重置模拟，清空所有状态和日志。

5. **查看结果**
   - 程序界面底部会实时显示缺页次数和缺页率。
   - 执行日志会记录每条指令的执行情况，包括是否缺页以及对应的物理地址。

## 示例

启动程序后，默认配置为320条指令和FIFO页面置换算法。点击“单步执行”按钮，将依次执行每条指令，并在日志中记录执行情况。内存块中会显示当前加载的页及其对应的指令地址。

## 设计思路

页面管理模拟器的设计思路主要包括以下几个方面：

1. **界面布局**：
   - 使用QVBoxLayout、QHBoxLayout和QGridLayout实现主窗口的布局，包括配置区域、内存展示区域、执行日志区域和控制按钮区域。
   
2. **功能实现**：
   - 使用QSpinBox配置总指令数，QRadioButton选择页面置换算法，QPushButton实现单步执行、连续执行和重置功能。
   - QLabel用于显示缺页次数和缺页率，QTextEdit用于记录执行日志。
   
3. **页面置换算法**：
   - FIFO（先进先出）：使用队列来管理内存中的页面，当内存满时，替换最先进入内存的页面。
   - LRU（最近最少使用）：使用栈来管理内存中的页面，当内存满时，替换最久未使用的页面。

## 代码分析

### 主类：PageManagementSimulator

#### 初始化方法：`__init__(self)`

- 调用`initUI`方法初始化用户界面。
- 调用`reset_simulation`方法重置模拟器状态。

#### 用户界面初始化方法：`initUI(self)`

- 配置区域：
  - 创建并配置QSpinBox控件，用于设置总指令数。
  - 创建并配置QRadioButton控件，用于选择页面置换算法。
  - 将上述控件添加到配置区域布局（QHBoxLayout）。
- 内存展示区域：
  - 使用QGridLayout布局，创建4个内存块，每个内存块包含10个不可点击的按钮，初始状态为“空”。
- 信息展示区域：
  - 创建QLabel控件，显示缺页次数和缺页率。
- 执行日志区域：
  - 创建QTextEdit控件，记录执行日志。
- 控制按钮区域：
  - 创建单步执行、连续执行和重置按钮，并绑定相应的事件处理方法。

#### 重置模拟器方法：`reset_simulation(self)`

- 初始化总指令数、缺页次数、已执行指令数、内存状态和算法相关的数据结构。
- 更新界面上的缺页次数和缺页率显示。
- 清空执行日志。

#### 页面置换算法实现

- **FIFO算法:** 使用`load_page_to_memory_fifo(self, page_number)`方法实现。
  - 如果内存有空闲位置，将页面加载到空闲位置，并添加到FIFO队列。
  - 如果内存已满，替换FIFO队列中最早进入的页面。
- **LRU算法:** 使用`load_page_to_memory_lru(self, page_number)`方法实现。
  - 如果内存有空闲位置，将页面加载到空闲位置，并添加到LRU堆栈。
  - 如果内存已满，替换LRU堆栈中最近最少使用的页面。

#### 指令执行方法：`execute_instruction(self)`

- 获取当前指令对应的页面号和指令地址。
- 判断页面是否在内存中，如果不在内存中，加载页面并记录缺页。
- 计算物理地址并更新内存块的显示状态。
- 更新指令执行日志。

#### 单步执行方法：`step_execution(self)`

- 执行当前指令并更新缺页率。
- 如果所有指令已执行完毕，弹出提示信息。

#### 连续执行方法：`run_execution(self)`

- 循环执行所有指令并实时更新缺页率。

#### 更新缺页率方法：`update_page_fault_rate(self)`

- 根据缺页次数和已执行指令数计算缺页率，并更新显示。
