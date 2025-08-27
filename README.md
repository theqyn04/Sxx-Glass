# Sxx Glass (Seg Glass) 🍷

Cài đặt Modelss (Seg Glass) 🍷

Ứng dụng AI chỉnh sửa ảnh anime với khả năng thay đổi trang phục. ⚠️Lưu ý rằng ứng dụng này chỉ dành cho mục đích nghiên cứu và sử dụng cá nhân. Diffusion WebUI (Automatic1111) có tính năng inpainting mạnh mẽ và cho phép vẽ mask trực tiếp.

**Mô hình segmentation** (phân vùng ảnh) để xác định đối tượng
**Stable Diffusion** để chỉnh sửa hoặc tạo ảnh dựa trên segmentation mask

## Cách sử dụng Stable Diffusion WebUI để xóa/quần áo?😈

Hãy chắc chắn python phải cài đúng bản 3.10.6.

Cài đặt Stable Diffusion WebUI:

```bash
  git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
  cd stable-diffusion-webui
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  pip install -r requirements.txt
```

Cài đặt Model👚:

* Download [MeinaHentai model](https://civitai.com/models/12606?modelVersionId=119992) vào thư mục ../stable-diffusion-webui/models/Stable-diffusion
* Sửa file webui-user.bat như sau và chạy:

```bash
  @echo off

  set PYTHON=
  set GIT=
  set VENV_DIR=
  set COMMANDLINE_ARGS= --precision full --no-half --opt-sub-quad-attention --lowvram --disable-nan-check

  call webui.bat
```

Chạy ứng dụng:

```bash
  run webui.bat
```

## Sử dụng Stable Diffusion WebUI trực tiếp

* Mở [http://127.0.0.1:7860/] hoặc [http://localhost:7860/] và vào tab img2img -> vào tab Inpaint -> Upload ảnh vào tô chỗ cần redraw 😉
* Nhớ tích Fill, Only masked
* Prompt nên dùng:
```bash
  positive: "nude, naked, no clothes, bare skin, high quality, detailed, big boobs"
  negative: "clothes, dressed, underwear, bra, panties, low quality, blurry"
```
* Cài đặt:
```bash
  Sampling method: DPM++ 2M Karras
  Steps: 20-30
  CFG scale: 7-10
  Denoising strength: 0.7-0.9
```
* Generate thoi :))
