import json
import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# --- إعدادات Supabase ---
SUPABASE_URL = "https://cewbmexcmhrogbvyfvrg.supabase.co/rest/v1/guests"
SUPABASE_KEY = "sb_publishable_MCDhff2Dztq4pp3ASoWX3A_inNp10mx"

class HotelApp(App):
    def build(self):
        # تفعيل وضع ملء الشاشة (Full Screen)
        Window.fullscreen = 'auto'
        
        # ملف التخزين المحلي
        self.config_file = "config.json"
        self.room_number = self.load_room_number()

        if not self.room_number:
            return self.setup_screen()
        else:
            return self.welcome_screen()

    def load_room_number(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f).get("room_number")
        return None

    def save_room_number(self, room_number):
        with open(self.config_file, "w") as f:
            json.dump({"room_number": room_number}, f)

    def setup_screen(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        layout.add_widget(Label(text="إعداد التطبيق", font_size='30sp', bold=True))
        layout.add_widget(Label(text="أدخل رقم الغرفة:", font_size='18sp'))
        
        self.room_input = TextInput(multiline=False, font_size='25sp', halign='center')
        layout.add_widget(self.room_input)
        
        save_btn = Button(text="حفظ واستمرار", size_hint_y=None, height='60dp', background_color=(0, 0.5, 1, 1))
        save_btn.bind(on_press=self.on_save)
        layout.add_widget(save_btn)
        
        return layout

    def on_save(self, instance):
        room = self.room_input.text.strip()
        if room:
            self.save_room_number(room)
            self.room_number = room
            self.root.clear_widgets()
            self.root.add_widget(self.welcome_screen())

    def welcome_screen(self):
        self.layout = BoxLayout(orientation='vertical', padding=100, spacing=20)
        
        # خلفية متدرجة (تغيير اللون)
        with self.layout.canvas.before:
            Color(0.12, 0.24, 0.45, 1) # لون أزرق داكن
            self.rect = Rectangle(size=Window.size, pos=self.layout.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)

        self.welcome_msg = Label(text="مرحباً بك", font_size='40sp', color=(0.8, 0.8, 0.8, 1))
        self.guest_name = Label(text="...", font_size='70sp', bold=True)
        self.footer = Label(text="نتمنى لك إقامة سعيدة", font_size='20sp', color=(0.6, 0.6, 0.6, 1))

        self.layout.add_widget(self.welcome_msg)
        self.layout.add_widget(self.guest_name)
        self.layout.add_widget(self.footer)

        # جلب البيانات من Supabase
        Clock.schedule_once(lambda dt: self.fetch_data(), 1)
        
        # إغلاق التطبيق بعد 12 ثانية (لإعطاء وقت للتحميل)
        Clock.schedule_once(lambda dt: self.stop(), 12)
        
        # إغلاق عند اللمس
        Window.bind(on_touch_down=lambda win, touch: self.stop())

        return self.layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def fetch_data(self):
        try:
            params = {"room_number": f"eq.{self.room_number}", "select": "full_name"}
            headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
            
            response = requests.get(SUPABASE_URL, params=params, headers=headers, timeout=5)
            data = response.json()
            
            if data and len(data) > 0:
                name = data[0].get("full_name", "أهلاً بك")
                self.guest_name.text = name if name else "أهلاً بك"
            else:
                self.guest_name.text = "أهلاً بك"
        except Exception as e:
            print(f"Error: {e}")
            self.guest_name.text = "أهلاً بك"

if __name__ == "__main__":
    HotelApp().run()
