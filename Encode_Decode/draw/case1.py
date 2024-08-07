import matplotlib.pyplot as plt
import numpy as np

# Tạo dữ liệu mẫu
distance = np.arange(0, 100, 10)
accuracy = np.exp(-distance / 50)  # Giả định tỉ lệ khung hình chính xác giảm theo hàm mũ với khoảng cách
error_rate = 1 - accuracy  # Giả định tỉ lệ dữ liệu sai nhận là 1 trừ đi tỉ lệ chính xác

# Tạo biểu đồ
fig, ax1 = plt.subplots()

# Vẽ đường cho tỉ lệ khung hình chính xác
color = 'tab:blue'
ax1.set_xlabel('Khoảng cách (m)')
ax1.set_ylabel('Tỉ lệ khung hình chính xác', color=color)
ax1.plot(distance, accuracy, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Thêm chú thích cho tỉ lệ khung hình chính xác
for i, txt in enumerate(accuracy):
    ax1.annotate(f'{txt:.2f}', (distance[i], accuracy[i]), textcoords="offset points", xytext=(0,10), ha='center', color=color)

# Tạo trục y thứ hai để vẽ tỉ lệ dữ liệu sai nhận
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Tỉ lệ dữ liệu sai nhận', color=color)
ax2.plot(distance, error_rate, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Thêm chú thích cho tỉ lệ dữ liệu sai nhận
for i, txt in enumerate(error_rate):
    ax2.annotate(f'{txt:.2f}', (distance[i], error_rate[i]), textcoords="offset points", xytext=(0,-15), ha='center', color=color)

# Thêm tiêu đề
plt.title('Mối quan hệ giữa khoảng cách và tỉ lệ khung hình chính xác/tỉ lệ dữ liệu sai nhận')

# Hiển thị biểu đồ
plt.show()
