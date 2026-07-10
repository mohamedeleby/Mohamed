from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import json
import os
import random
from aribc import fix_arabic

Window.clearcolor=(0,0,100/255,1)

class Mygams(Widget):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
      # الكلام الي هيظهر بالعربي
       self.arabic1_text = fix_arabic(" ركذ ونبي هموت")
       self.arabic2_text = fix_arabic(" ركذ انا كده هموت")
       self.arabic3_text = fix_arabic("يا غبي ما انت لسه مختار نفس الحرف")
       self.arabic4_text = fix_arabic("عدد المحولات")
       self.arabic5_text = fix_arabic("انت كسبت ")
       self.arabic6_text = fix_arabic("فهمان")
       self.arabic7_text = fix_arabic("موت بسببك يا غبي")
       self.arabic8_text = fix_arabic("تحب تالعب تاني ")
       self.arabic9_text = fix_arabic("وله زهقت")
       self.arabic10_text = fix_arabic("الكلمه كانت")
       
      # القائمه الي فيه الاشكال المشنقه
       self.hangman_stages= ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
      # عدد المحولات 
       self.laeve=6
      #الحروف الي هو اختاره غلط 
       self.letterappend=[]
      #الكلامات با لاوصف
       self.words={
    "تفاح": "فاكهة مدورة لونها أحمر أو أخضر وطعمها مسكر",
    "موز": "فاكهة طويلة لونها أصفر وبنحب نقشرها",
    "برتقال": "فاكهة برتقالية غنية بفيتامين سي وشكلها كروي",
    "بطيخ": "فاكهة كبيرة لونها أخضر من بره وأحمر من جوه",
    "عنب": "فاكهة صغيرة بتيجي في عناقيد ولونها بنفسجي أو أخضر",
    "فراولة": "فاكهة حمراء صغيرة عليها نقط سودة وطعمها لذيذ",
    "مانجو": "ملك الفواكه، لونها أصفر أو برتقالي وطعمها استوائي",
    "اناناس": "فاكهة قشرتها خشنة ومن جوه لونها أصفر وليها زعبوط أخضر",
    "رمان": "فاكهة حمراء مليانة حبيبات صغيرة زي اللولي",
    "ليمون": "فاكهة لونها أصفر وطعمها حامض جداً",
    "خيار": "خضروات لونها أخضر وبنحطها في السلطة",
    "جزر": "خضروات برتقالية مفيدة للنظر وتقوي العين",
    "طماطم": "خضروات حمراء مدورة بنعمل منها الصلصة",
    "بطاطس": "خضروات بنقليها وبنعمل منها شيبسي",
    "بصل": "خضروات بتخلينا نعيط لما بنقطعها",
    "كيكة": "حلويات بنعملها في أعياد الميلاد بالدقيق والسكر",
    "بسبوسة": "حلويات شرقية مرملة وعليها شربات",
    "كنافة": "حلويات مشهورة في رمضان وبتبقي مقرمشة",
    "شوكولاتة": "حلويات لونها بني وكل الناس بتحبها",
    "ايس كريم": "حلويات ساقعة جداً وبناكلها في الصيف",
    "اسد": "ملك الغابة وعنده زئير قوي جداً",
    "فيل": "حيوان ضخم جداً وعنده زلومة طويلة",
    "زرافة": "حيوان رقبته طويلة جداً وبياكل ورق الشجر",
    "نمر": "حيوان سريع جداً وجسمه مخطط بالأسود",
    "طبيب": "مهنة الشخص اللي بيعالج المرضى في المستشفى",
    "مهندس": "شخص بيبني البيوت والكباري وبيرسم الخطط",
    "معلم": "شخص بيشرح الدروس للطلاب في المدرسة",
    "طيار": "شخص بيسوق الطيارة وبيسافر بين البلاد",
    "مصر": "دولة عربية فيها الأهرامات ونهر النيل",
    "السعودية": "دولة عربية فيها الكعبة المشرفة",
    "فلسطين": "دولة عربية عاصمتها القدس الشريف",
    "ملاقة": "أداة بناكل بيها الرز والشوربة",
    "مقص": "أداة بنستخدمها عشان نقص الورق والقماش",
    "مفتاح": "حاجة صغيرة بنفتح بيها الباب",
    "قلم": "أداة بنكتب بيها في الكراسة",
    "مروحة": "جهاز بيطلع هوا ساقع في الصيف",
    "ثلاجة": "جهاز بنحفظ فيه الأكل عشان ما يبوظش"
}  
      #عدد المرات الي كسب فيه 
       self.number=0
      #الاقائمه الي بينضاف فيه الكلمه عشان ما تتكرش 
       self.available_words = list(self.words.keys())
      #الدله الي بخد الكلام من القائمه و تحطه في الملف
       self.load_game_data()
      #بتشغل اللعبه
       self.pick_new_word()


   def save_data(self):
      self.data_to_save = {
        "rem_words": self.available_words
        
      }
      # بنفتح ملف اسمه save_data.json للكتابة ("w")
      with open("main.py/lest.json", "w", encoding="utf-8") as f:
        # بنقول للـ json: خد البيانات دي وحطها في الملف
        json.dump(self.data_to_save, f, ensure_ascii=False, indent=4)
        
   def load_game_data(self):
    # بنشوف هل الملف موجود أصلاً؟
     if os.path.exists("main.py/lest.json"):
        with open("main.py/lest.json", "r", encoding="utf-8") as f:
            saved_data = json.load(f) # بنقرأ البيانات
            
            # بنأخد الكلمات اللي كانت فاضلة
            remaining = saved_data.get("rem_words", [])
            
            # لو القائمة مش فاضية، رجعها للعبة
            if remaining:
                return remaining
    
    # لو الملف مش موجود (أول مرة نلعب) نرجع القائمة كاملة
     return list(self.words.keys())
   
   def pick_new_word(self):
    # التأكد إن القائمة مش فاضية
       if len(self.available_words) > 0:
        # اختيار كلمة عشوائية من المتاح
         
         self.ids.mylabel3.text =f' {self.number} : {self.arabic5_text}'
         self.random_word = random.choice(self.available_words)
         self.Empty=["_"]*len(self.random_word)
         self.ids.ch.text = "".join(self.Empty)
         self.ids.mylabel.text= (f"\n{self.arabic1_text} \n \n{self.arabic4_text}  : {self.laeve}  ")
         self.ids.mylabel2.text = self.hangman_stages[6-self.laeve] 
        
        # أهم خطوة: حذف الكلمة من القائمة المتاحة
         self.available_words.remove(self.random_word)
         self.save_data()
        
        # تجيب التلميح بتاع الكلمة اللي اخترناها
         self.word_hint = self.words[self.random_word]
        
        # تحديث الواجهة (العربي)
         self.ids.hint_label.text = fix_arabic(self.word_hint)
        
       else:
        # لو القائمة خلصت، ممكن تعيد شحنها أو تنهي اللعبة
          self.ids.hint_label.text = fix_arabic("خلصت كل الفواكه! هنبدأ من جديد")
          self.available_words = list(self.words.keys())
          self.pick_new_word() # ابدأ من جديد تلقائياً
   def show_game_over_popup(self, title_text):
      # 1. بنعمل المنظم اللي هيشيل الزراير
      content = BoxLayout(orientation='vertical', padding=10, spacing=10)
      # 2. بنضيف رسالة
      content.add_widget(Label(text=f" {self.arabic11_text} : {self.arabic10_text}"))
      # 3. بنعمل زراير الاختيارات
      btn_layout = BoxLayout(spacing=10)
      re_btn = Button(text=self.arabic8_text)
      re_btn.bind(on_release=self.reset_game) # هنربطها بدالة إعادة اللعبة
      exit_btn = Button(text=self.arabic9_text )
      exit_btn.bind(on_release=App.get_running_app().stop) # بتقفل البرنامج
      btn_layout.add_widget(re_btn)
      btn_layout.add_widget(exit_btn)
      content.add_widget(btn_layout)
      # 4. بننشئ الـ Popup ونفتحه
      self.popup = Popup(title=title_text, content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
      self.popup.title_font = "main.py/arialbd.ttf"
      self.popup.open()

   def reset_game(self, *args):
    # دالة عشان تصفر اللعبة من جديد
     self.letterappend=[]
     self.laeve = 6
     self.number=0
     self.ids.mylabel.color="#ffffff"
     self.popup.dismiss() # بنقفل النافذة
     self.load_game_data()
     self.pick_new_word()
     self.gime=False
    
    
    
    
   def button (self,letter):   
      self.gime=True
      if letter in self.letterappend:
          self.ids.mylabel.text=(f" \n{self.arabic3_text} \n    {self.arabic4_text}  : {self.laeve}")
          self.gime=False 
      elif "_" in self.Empty and self.laeve==0:
            self.arabic11_text = fix_arabic(self.random_word)
            self.show_game_over_popup(self.arabic7_text)
            self.load_game_data()
            self.pick_new_word()

      while "_" in self.Empty and self.laeve > 0 and self.gime==True:    
          if  letter not in self.random_word:
            self.laeve-=1
            self.ids.mylabel2.text=(f" {self.hangman_stages[6-self.laeve]}")
            self.ids.mylabel.text=(f"{self.arabic2_text} \n \n   {self.arabic4_text}  :   {self.laeve}")
            self.ids.mylabel.color="#ff0000"
            self.letterappend.append(letter)
            self.gime=False
          else:
            for i in range(len(self.random_word)):
              if self.random_word [i] ==letter:
                  self.Empty[i]=letter
                  self.ids.ch.text=fix_arabic("".join(self.Empty))
                  
                  if "_" not in self.Empty:
                    self.number+=1
                    self.letterappend=[]
                    self.load_game_data()
                    self.pick_new_word()
                  self.gime=False   
        
        
            

class MyApp (App):
    def build(self):
        self.title="هايدي"
        return Mygams()
    
if __name__ =="__main__":
    MyApp().run()    
