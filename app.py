import streamlit as st
import subprocess
import os

# إعداد واجهة الصفحة
st.set_page_config(page_title="BS Video Master", layout="centered")

# تصميم الواجهة (CSS بسيط لجعلها أنيقة)
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎥 محرك معالجة فيديوهات تيك توك (BS)")
st.write("ارفع مقطعك الآن ليتم تبطيئه ورفع جودته بتقنية FFmpeg")

# خانة رفع الفيديو
uploaded_file = st.file_uploader("اختر مقطع الفيديو هنا", type=["mp4", "mov"])

if uploaded_file is not None:
    # حفظ الفيديو المرفوع مؤقتاً
    input_path = "input_video.mp4"
    output_path = "BS_60FPS_Slow.mp4"
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("تم رفع الفيديو بنجاح.. اضغط على الزر للبدء.")

    if st.button("بدء المعالجة (جودة عالية + 60fps)"):
        with st.spinner("جاري المعالجة الآن.. يرجى الانتظار"):
            # أمر FFmpeg الاحترافي:
            # 1. يبطئ الفيديو (0.5x)
            # 2. يرفع الـ FPS إلى 60 لخداع التيك توك
            # 3. يحافظ على جودة سينمائية (CRF 18)
            command = [
                'ffmpeg', '-y', '-i', input_path,
                '-vf', "setpts=2.0*PTS",  # تبطيء المقطع للضعف
                '-r', '60',               # تحويله إلى 60 إطار
                '-c:v', 'libx264',
                '-crf', '18',             # جودة عالية جداً
                '-preset', 'fast',
                '-pix_fmt', 'yuv420p',
                output_path
            ]
            
            try:
                subprocess.run(command, check=True)
                
                # عرض النتيجة وزر التحميل
                st.success("✅ تمت المعالجة بنجاح!")
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 تحميل الفيديو ونشره على تيك توك",
                        data=file,
                        file_name="BS_TikTok_Quality.mp4",
                        mime="video/mp4"
                    )
                st.balloons()
            except Exception as e:
                st.error("حدث خطأ أثناء المعالجة، تأكد من جودة الفيديو المرفوع.")

st.markdown("---")
st.caption("جميع الحقوق محفوظة لمتجر BS")
