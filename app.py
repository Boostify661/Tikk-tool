import streamlit as st
import subprocess
import os
import shutil

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="BS Video Master", layout="centered")

# 2. نظام الأكواد وقفل الجهاز (10 أكواد)
# ملاحظة: سيتم قفل الكود على أول جهاز (Browser) يدخل به العميل
if "codes_db" not in st.session_state:
    st.session_state["codes_db"] = {
        "BS-7710": None,
        "BS-8820": None,
        "BS-9930": None,
        "PRO-TIK-1": None,
        "PRO-TIK-2": None,
        "VIP-MASTER": None,
        "BS-SPEED-1": None,
        "BS-SPEED-2": None,
        "GOLD-USER": None,
        "PREMIUM-BS": None
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# تنسيق بسيط بالـ CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 25px; background-color: #007bff; color: white; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { text-align: center; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎥 محرك معالجة فيديوهات (BS)")
st.subheader("جودة عالية + 60 إطار في الثانية")

# 3. منطق التحقق من الدخول
if not st.session_state["authenticated"]:
    st.info("مرحباً بك! يرجى إدخال كود التفعيل الخاص بك لاستخدام الأداة.")
    user_code = st.text_input("كود الدخول", type="password", placeholder="أدخل الكود هنا...")
    
    if st.button("تفعيل الدخول ✨"):
        # الحصول على بصمة الجهاز (المتصفح)
        device_id = st.context.headers.get("User-Agent")
        
        if user_code in st.session_state["codes_db"]:
            # حالة 1: الكود جديد ولم يستخدم بعد
            if st.session_state["codes_db"][user_code] is None:
                st.session_state["codes_db"][user_code] = device_id
                st.session_state["authenticated"] = True
                st.success("تم تفعيل الكود وربطه بجهازك الحالي بنجاح!")
                st.rerun()
            
            # حالة 2: الكود مستخدم، نتأكد إذا كان نفس الجهاز
            elif st.session_state["codes_db"][user_code] == device_id:
                st.session_state["authenticated"] = True
                st.rerun()
            
            # حالة 3: الكود مستخدم على جهاز آخر
            else:
                st.error("⚠️ عذراً، هذا الكود مفعّل مسبقاً على جهاز آخر. لا يمكن استخدامه.")
        else:
            st.error("❌ الكود الذي أدخلته غير صحيح.")

else:
    # 4. واجهة الأداة بعد نجاح الدخول
    st.success("✅ الكود يعمل! يمكنك الآن رفع فيديوهاتك.")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    # التأكد من وجود محرك FFmpeg
    if shutil.which("ffmpeg") is None:
        st.error("⚠️ خطأ تقني: محرك المعالجة FFmpeg غير مثبت. تأكد من وجود ملف packages.txt وعمل Reboot للأداة.")
    else:
        uploaded_file = st.file_uploader("اختر مقطع الفيديو من جهازك", type=["mp4", "mov"])

        if uploaded_file is not None:
            input_path = "temp_input.mp4"
            output_path = "BS_PRO_60FPS.mp4"
            
            # حفظ الملف المرفوع مؤقتاً
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if st.button("🚀 ابدأ المعالجة الاحترافية"):
                with st.spinner("جاري تبطئ الفيديو ورفع الجودة.. يرجى الانتظار"):
                    # أمر المعالجة (تحويل لـ 60 إطار + جودة عالية CRF 18)
                    command = f'ffmpeg -y -i "{input_path}" -vf "setpts=2.0*PTS" -r 60 -c:v libx264 -crf 18 -preset fast "{output_path}"'
                    
                    process = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    if process.returncode == 0:
                        st.success("✨ تمت المعالجة بنجاح!")
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="📥 تحميل الفيديو المعالج",
                                data=file,
                                file_name="BS_Video_60FPS.mp4",
                                mime="video/mp4"
                            )
                        st.balloons()
                    else:
                        st.error("حدث خطأ أثناء المعالجة، تأكد من جودة المقطع المرفوع.")
                        with st.expander("تفاصيل الخطأ"):
                            st.code(process.stderr)

st.markdown("---")
st.caption("جميع الحقوق محفوظة لمتجر BS © 2026")
