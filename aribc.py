import arabic_reshaper
from bidi.algorithm import get_display

# دالة لتحويل النص العربي ليظهر بشكل صحيح
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text) # ربط الحروف
    bidi_text = get_display(reshaped_text)      # عكس الاتجاه
    return bidi_text
