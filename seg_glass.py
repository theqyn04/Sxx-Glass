import streamlit as st
import torch
import numpy as np
from PIL import Image
import cv2
from diffusers import StableDiffusionInpaintPipeline
import time

# Tiêu đề ứng dụng
st.title("🎨 AI Chỉnh sửa Ảnh Anime (Local Use Only)")
st.warning("⚠️ ỨNG DỤNG CHỈ DÀNH CHO NGHIÊN CỨU CÁ NHÂN - KHÔNG CHIA SẺ RA NGOÀI")

# Tải mô hình
@st.cache_resource
def load_models():
    try:
        with st.spinner('Đang tải mô hình AI (lần đầu có thể mất 10-15 phút)...'):
            # Tải mô hình Stable Diffusion để inpaint
            inpainting_pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "stabilityai/stable-diffusion-2-inpainting",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            if torch.cuda.is_available():
                inpainting_pipe = inpainting_pipe.to("cuda")
            
            st.success("Đã tải xong mô hình!")
            return inpainting_pipe
            
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình: {str(e)}")
        return None

# Hàm tạo mask cho vùng quần áo (demo)
def create_clothing_mask(image, mode="upper"):
    # Chuyển ảnh sang numpy array
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    # Tạo mask rỗng
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # Xác định vùng cơ thể dựa trên màu da (ước lượng)
    # Đây là phương pháp đơn giản, trong thực tế cần model segmentation tốt hơn
    if len(img_array.shape) == 3:
        # Chuyển sang HSV để dễ nhận diện màu da
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Phạm vi màu da ước lượng (cần điều chỉnh cho ảnh anime)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Xác định vùng quần áo dựa trên vùng không phải da
        if mode == "upper":
            # Vùng trên cơ thể (áo)
            cv2.rectangle(mask, (width//4, height//4), (3*width//4, 3*height//5), 255, -1)
        elif mode == "lower":
            # Vùng dưới cơ thể (quần)
            cv2.rectangle(mask, (width//4, 3*height//5), (3*width//4, 4*height//5), 255, -1)
        else:
            # Toàn bộ quần áo
            cv2.rectangle(mask, (width//4, height//4), (3*width//4, 4*height//5), 255, -1)
            
        # Loại bỏ vùng da từ mask quần áo
        mask[skin_mask > 0] = 0
        
    return Image.fromarray(mask)

# Hàm chỉnh sửa ảnh với prompt
def edit_image_with_prompt(image, mask, prompt, pipe, strength=0.8):
    try:
        # Chuẩn bị ảnh và mask
        image = image.resize((512, 512))
        mask = mask.resize((512, 512))
        
        # Chỉnh sửa ảnh
        result = pipe(
            prompt=prompt,
            image=image,
            mask_image=mask,
            strength=strength,
            guidance_scale=7.5,
            num_inference_steps=30,
        ).images[0]
        
        return result
    except Exception as e:
        st.error(f"Lỗi khi chỉnh sửa ảnh: {str(e)}")
        return image

# Tải mô hình
inpainting_pipe = load_models()

# Tải lên ảnh
uploaded_file = st.file_uploader("Chọn ảnh anime...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mở ảnh
    image = Image.open(uploaded_file).convert("RGB")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Ảnh gốc", use_column_width=True)
    
    # Chọn vùng chỉnh sửa
    clothing_area = st.radio("Chọn vùng muốn chỉnh sửa:", 
                           ["Áo", "Quần", "Toàn bộ trang phục"])
    
    mode_map = {"Áo": "upper", "Quần": "lower", "Toàn bộ trang phục": "full"}
    
    # Tạo mask
    mask = create_clothing_mask(image, mode_map[clothing_area])
    
    with col2:
        # Hiển thị mask
        mask_display = np.array(mask)
        mask_display = np.stack([mask_display, mask_display, mask_display], axis=-1)
        st.image(mask_display, caption="Vùng sẽ được chỉnh sửa (màu trắng)", 
                 use_column_width=True)
    
    # Chọn loại trang phục mới
    outfit_options = {
        "Áo swimsuit": "swimsuit, bikini, beachwear",
        "Áo dạ hội": "elegant dress, evening gown, formal wear",
        "Đồng phục học sinh": "school uniform, sailor outfit, anime school uniform",
        "Trang phục thể thao": "sportswear, athletic outfit, gym clothes",
        "Trang phục cosplay": "fantasy outfit, cosplay costume, anime costume",
        "Tùy chỉnh": "nhập mô tả của bạn"
    }
    
    outfit_choice = st.selectbox("Chọn loại trang phục thay thế:", list(outfit_options.keys()))
    
    if outfit_choice == "Tùy chỉnh":
        custom_prompt = st.text_input("Nhập mô tả trang phục mới:")
        prompt = custom_prompt if custom_prompt else "new outfit, anime style"
    else:
        prompt = outfit_options[outfit_choice]
    
    # Cường độ chỉnh sửa
    strength = st.slider("Cường độ chỉnh sửa:", 0.1, 1.0, 0.8)
    
    # Chỉnh sửa ảnh
    if st.button("✨ Tạo trang phục mới"):
        if inpainting_pipe is None:
            st.warning("Mô hình AI chưa được tải đầy đủ. Vui lòng chờ...")
        else:
            with st.spinner("AI đang tạo trang phục mới (có thể mất 1-2 phút)..."):
                result = edit_image_with_prompt(image, mask, prompt, inpainting_pipe, strength)
            
            # Hiển thị kết quả
            st.image(result, caption="Ảnh đã chỉnh sửa", use_column_width=True)
            
            # Lưu ảnh
            result.save("edited_anime_image.png")
            with open("edited_anime_image.png", "rb") as file:
                st.download_button(
                    label="💾 Tải ảnh đã chỉnh sửa",
                    data=file,
                    file_name="anime_with_new_outfit.png",
                    mime="image/png"
                )
else:
    st.info("Vui lòng tải lên ảnh anime để bắt đầu.")

# Giải thích kỹ thuật
st.markdown("---")
st.header("🔍 Giải thích kỹ thuật")
st.write("""
Ứng dụng sử dụng mô hình Stable Diffusion Inpainting để thay thế trang phục:

1. **Nhận diện vùng quần áo**: Sử dụng kỹ thuật xử lý ảnh để xác định vùng quần áo cần thay thế
2. **Tạo mask**: Tạo mặt nạ xác định vùng sẽ được chỉnh sửa
3. **Tạo nội dung mới**: Dựa trên prompt mô tả, AI tạo trang phục mới phù hợp với ngữ cảnh
4. **Kết hợp ảnh**: Ghép nội dung mới vào ảnh gốc một cách tự nhiên

**Lưu ý**: Kết quả phụ thuộc vào chất lượng ảnh đầu vào và mô tả prompt.
""")

# Cảnh báo đạo đức
st.markdown("---")
st.header("🚫 Cảnh báo quan trọng")
st.error("""
ỨNG DỤNG NÀY CHỈ ĐƯỢC SỬ DỤNG CHO MỤC ĐÍCH:
- Nghiên cứu học thuật về AI
- Phát triển kỹ thuật xử lý ảnh
- Sử dụng cá nhân với ảnh của chính mình

KHÔNG SỬ DỤNG ĐỂ:
- Tạo nội dung khiêu dâm
- Xâm phạm quyền riêng tư người khác
- Chia sẻ nội dung nhạy cảm
""")