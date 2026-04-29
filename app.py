import streamlit as st
import subprocess
import os

# إعداد واجهة الصفحة
st.set_page_config(page_title="BS Video Master", layout="centered")

# --- قائمة أكواد الدخول ---
# أضف هنا كل الأكواد التي تريدها بين الفواصل
VALID_CODES = ["BSF$91", "BSF$88", "BSF$2", "BSF$1","BSF€16"] 

st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎥 محرك معالجة فيديوهات (BS)")

# التحقق من الجلسة
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.info("مرحباً بك! يرجى إدخال كود التفعيل المرفق مع طلبك.")
    user_code = st.text_input("أدخل كود الدخول:", type="password")
    
    if st.button("تفعيل الدخول ✨"):
        if user_code in VALID_CODES: # هنا يتأكد إذا الكود موجود في القائمة
            st.session_state["authenticated"] = True
            st.success("تم التفعيل بنجاح!")
            st.rerun()
        else:
            st.error("الكود غير صحيح أو منتهي الصلاحية.")
else:
    # --- واجهة الأداة بعد الدفع والدخول ---
    st.success("✅ الكود يعمل! يمكنك الآن رفع ومعالجة فيديوهاتك.")
    
    if st.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    uploaded_file = st.file_uploader("اختر مقطع الفيديو هنا", type=["mp4", "mov"])

    if uploaded_file is not None:
        input_path = "input_video.mp4"
        output_path = "BS_60FPS_Slow.mp4"
        
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("بدء المعالجة (جودة عالية + 60fps)"):
            with st.spinner("جاري المعالجة.. يرجى عدم إغلاق الصفحة"):
                command = [
                    'ffmpeg', '-y', '-i', input_path,
                    '-vf', "setpts=2.0*PTS",
                    '-r', '60',
                    '-c:v', 'libx264',
                    '-crf', '18',
                    '-preset', 'fast',
                    '-pix_fmt', 'yuv420p',
                    output_path
                ]
                
                try:
                    subprocess.run(command, check=True)
                    st.success("✅ تمت المعالجة بنجاح!")
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 تحميل الفيديو الآن",
                            data=file,
                            file_name="BS_Processed.mp4",
                            mime="video/mp4"
                        )
                    st.balloons()
                except Exception as e:
                    st.error("حدث خطأ، تأكد من ملف الفيديو.")
