from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from openai import OpenAI

CHAVE_API = "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"
client = OpenAI(base_url="https://openrouter.ai", api_key=CHAVE_API)
historico = [{"role": "assistant", "content": "Olá! Sou o J BOT em Kivy."}]

class JBotChat(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_logs = Label(text="J BOT: Olá! Sou o J BOT.\n", size_hint_y=None, valign='top', halign='left')
        self.chat_logs.bind(texture_size=self.chat_logs.setter('size'))
        self.chat_logs.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.scroll.add_widget(self.chat_logs)
        self.add_widget(self.scroll)
        self.bottom_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        self.entrada = TextInput(hint_text="Digite aqui...", multiline=False)
        self.entrada.bind(on_text_validate=self.enviar_mensagem)
        self.botao = Button(text="Enviar", size_hint=(0.25, 1))
        self.botao.bind(on_release=self.enviar_mensagem)
        self.bottom_row.add_widget(self.entrada)
        self.bottom_row.add_widget(self.botao)
        self.add_widget(self.bottom_row)

    def enviar_mensagem(self, instance):
        texto = self.entrada.text.strip()
        if not texto: return
        historico.append({"role": "user", "content": texto})
        self.chat_logs.text += f"\nVocê: {texto}\n"
        self.entrada.text = ""
        try:
            response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=historico)
            resposta_ia = response.choices.message.content
            self.chat_logs.text += f"\nJ BOT: {resposta_ia}\n"
            historico.append({"role": "assistant", "content": resposta_ia})
        except Exception as erro:
            self.chat_logs.text += f"\nErro: {erro}\n"

class MainApp(App):
    def build(self): return JBotChat()

if __name__ == "__main__": MainApp().run()

