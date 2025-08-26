# Sxx Glass (Seg Glass)

Ứng dụng AI chỉnh sửa ảnh anime với khả năng thay đổi trang phục. Lưu ý rằng ứng dụng này chỉ dành cho mục đích nghiên cứu và sử dụng cá nhân.

**Mô hình segmentation** (phân vùng ảnh) để xác định đối tượng
**Stable Diffusion** để chỉnh sửa hoặc tạo ảnh dựa trên segmentation mask

## Chạy code như thế nào?

Cài đặt các thư viện cần thiết:

```bash
  pip install torch torchvision torchaudio
  pip install diffusers transformers streamlit opencv-python pillow
  pip install streamlit-drawable-canvas
```

Chạy ứng dụng:

```bash
  streamlit run seg_glass.py
```
