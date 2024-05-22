import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QTextEdit, QSpinBox, QMessageBox, QGridLayout

class PageManagementSimulator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.reset_simulation()

    def initUI(self):
        # 总体布局
        main_layout = QVBoxLayout()
        config_layout = QHBoxLayout()
        
        # 设置区域
        config_layout.addWidget(QLabel('总指令数:'))
        self.instruction_count_spinbox = QSpinBox()
        self.instruction_count_spinbox.setRange(1, 320)  # 设置总指令数范围为1到320
        self.instruction_count_spinbox.setValue(320)
        config_layout.addWidget(self.instruction_count_spinbox)

        self.fifo_radio = QRadioButton('FIFO')
        self.fifo_radio.setChecked(True)
        self.lru_radio = QRadioButton('LRU')
        self.algo_group = QButtonGroup()
        self.algo_group.addButton(self.fifo_radio)
        self.algo_group.addButton(self.lru_radio)
        config_layout.addWidget(QLabel('页面置换算法:'))
        config_layout.addWidget(self.fifo_radio)
        config_layout.addWidget(self.lru_radio)

        main_layout.addLayout(config_layout)

        # 内存展示区域
        self.memory_layout = QGridLayout()
        self.memory_blocks = [[QPushButton('空') for _ in range(10)] for _ in range(4)]
        self.memory_labels = [QLabel(f'内存块 {i+1}') for i in range(4)]

        for i in range(4):
            self.memory_layout.addWidget(self.memory_labels[i], i, 0)
            for j in range(10):
                self.memory_blocks[i][j].setEnabled(False)
                self.memory_layout.addWidget(self.memory_blocks[i][j], i, j + 1)

        main_layout.addLayout(self.memory_layout)

        self.page_fault_label = QLabel('缺页次数: 0')
        self.page_fault_rate_label = QLabel('缺页率: 0.00%')
        main_layout.addWidget(self.page_fault_label)
        main_layout.addWidget(self.page_fault_rate_label)

        # 执行日志区域
        self.log_text_edit = QTextEdit()
        main_layout.addWidget(self.log_text_edit)

        # 控制按钮区域
        control_layout = QHBoxLayout()
        self.step_button = QPushButton('单步执行')
        self.run_button = QPushButton('连续执行')
        self.reset_button = QPushButton('重置')
        control_layout.addWidget(self.step_button)
        control_layout.addWidget(self.run_button)
        control_layout.addWidget(self.reset_button)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

        # 绑定按钮事件
        self.step_button.clicked.connect(self.step_execution)
        self.run_button.clicked.connect(self.run_execution)
        self.reset_button.clicked.connect(self.reset_simulation)

    def reset_simulation(self):
        self.total_instructions = self.instruction_count_spinbox.value()
        self.page_faults = 0
        self.executed_instructions = 0
        self.memory = [-1] * 4
        self.fifo_queue = []
        self.lru_stack = []
        self.instructions_executed = 0

        self.page_fault_label.setText('缺页次数: 0')
        self.page_fault_rate_label.setText('缺页率: 0.00%')
        self.log_text_edit.clear()

        for i in range(4):
            self.memory_labels[i].setText(f'内存块 {i+1}')
            for j in range(10):
                self.memory_blocks[i][j].setText('空')
                self.memory_blocks[i][j].setStyleSheet("")

        self.current_instruction_index = random.randint(0, self.total_instructions - 1)

    def get_page_number(self, instruction_index):
        return instruction_index // 10

    def is_page_in_memory(self, page_number):
        return page_number in self.memory

    def load_page_to_memory_fifo(self, page_number):
        replaced_page = None
        if -1 in self.memory:
            free_index = self.memory.index(-1)
            self.memory[free_index] = page_number
            self.fifo_queue.append(page_number)
        else:
            replaced_page = self.fifo_queue.pop(0)
            oldest_page_index = self.memory.index(replaced_page)
            self.memory[oldest_page_index] = page_number
            self.fifo_queue.append(page_number)
        self.page_faults += 1
        return replaced_page

    def load_page_to_memory_lru(self, page_number):
        replaced_page = None
        if -1 in self.memory:
            free_index = self.memory.index(-1)
            self.memory[free_index] = page_number
            self.lru_stack.append(page_number)
        else:
            replaced_page = self.lru_stack.pop(0)
            lru_page_index = self.memory.index(replaced_page)
            self.memory[lru_page_index] = page_number
            self.lru_stack.append(page_number)
        self.page_faults += 1
        return replaced_page

    def load_page_to_memory(self, page_number):
        if self.fifo_radio.isChecked():
            return self.load_page_to_memory_fifo(page_number)
        else:
            return self.load_page_to_memory_lru(page_number)

    def execute_instruction(self):
        current_page = self.get_page_number(self.current_instruction_index)
        instruction_address = self.current_instruction_index

        if not self.is_page_in_memory(current_page):
            replaced_page = self.load_page_to_memory(current_page)
            self.log_text_edit.append(f'{self.instructions_executed + 1}: 指令 {instruction_address} 缺页, 换出页 {replaced_page if replaced_page is not None else "无"}, 换入页 {current_page}')
        else:
            self.log_text_edit.append(f'{self.instructions_executed + 1}: 指令 {instruction_address} 命中, 页 {current_page}')

        physical_address = self.memory.index(current_page) * 10 + (instruction_address % 10)
        self.log_text_edit.append(f'物理地址: {physical_address}')
        
        for i in range(4):
            if self.memory[i] != -1:
                page_number = self.memory[i]
                self.memory_labels[i].setText(f'内存块 {i+1}: 页 {page_number}')
                for j in range(10):
                    instruction_addr = page_number * 10 + j
                    self.memory_blocks[i][j].setText(str(instruction_addr))
                    self.memory_blocks[i][j].setStyleSheet("")
            else:
                self.memory_labels[i].setText(f'内存块 {i+1}')
                for j in range(10):
                    self.memory_blocks[i][j].setText('空')
                    self.memory_blocks[i][j].setStyleSheet("")

        row = physical_address // 10
        col = physical_address % 10
        self.memory_blocks[row][col].setStyleSheet("background-color: red")

        self.instructions_executed += 1
        self.determine_next_instruction()

    def determine_next_instruction(self):
        prob = random.random()
        total_instructions = self.total_instructions
        if prob < 0.5:
            self.current_instruction_index = (self.current_instruction_index + 1) % total_instructions
        elif prob < 0.75:
            if self.current_instruction_index > 0:
                self.current_instruction_index = random.randint(0, self.current_instruction_index - 1) % total_instructions
            else:
                self.current_instruction_index = 0
        else:
            if self.current_instruction_index < total_instructions - 1:
                self.current_instruction_index = random.randint(self.current_instruction_index + 1, total_instructions - 1) % total_instructions
            else:
                self.current_instruction_index = total_instructions - 1


    def step_execution(self):
        if self.instructions_executed < self.total_instructions:
            self.execute_instruction()
            self.update_page_fault_rate()
        else:
            QMessageBox.information(self, '信息', '所有指令已执行完毕。')

    def run_execution(self):
        while self.instructions_executed < self.total_instructions:
            self.execute_instruction()
            self.update_page_fault_rate()

    def update_page_fault_rate(self):
        if self.instructions_executed > 0:
            fault_rate = (self.page_faults / self.instructions_executed) * 100
            self.page_fault_label.setText(f'缺页次数: {self.page_faults}')
            self.page_fault_rate_label.setText(f'缺页率: {fault_rate:.2f}%')
        else:
            self.page_fault_label.setText('缺页次数: 0')
            self.page_fault_rate_label.setText('缺页率: 0.00%')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PageManagementSimulator()
    ex.setWindowTitle('页面管理模拟器')
    ex.resize(800, 600)
    ex.show()
    sys.exit(app.exec_())
