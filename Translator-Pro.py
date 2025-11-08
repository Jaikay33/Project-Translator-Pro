# Project-Translator-Pro
# its a GUI App Named "Translator Pro" using python , Tkinter library, deep_translator library as GoogleTranslator library &amp; CTK library. 

import customtkinter as ctk
from tkinter import messagebox
from deep_translator import GoogleTranslator
import threading

ctk.set_appearance_mode("dark")   
ctk.set_default_color_theme("green") 

app = ctk.CTk()
app.title("🌍 Translator Pro")
app.geometry("900x550")
app.resizable(False, False)

FONT_MAIN = ("Segoe UI", 13)
FONT_BOLD = ("Segoe UI", 14, "bold")

try:
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
except Exception as e:
    messagebox.showerror("Initialization Error", f"Failed to fetch languages: {str(e)}")
    langs_dict = {"english": "en", "urdu": "ur"}  

lang_names = ["auto (detect)"] + sorted(langs_dict.keys(), key=str.lower)

def translate_text():
    def worker():
        try:
            source_text = text_input.get("0.0", "end").strip()
            if not source_text:
                messagebox.showwarning("Input Error", "Please enter text to translate.")
                restore_button()
                return

            src_sel = combo_source.get()
            dest_sel = combo_target.get()

            src_lang = 'auto' if src_sel == "auto (detect)" else langs_dict.get(src_sel.lower())
            dest_lang = langs_dict.get(dest_sel.lower())

            if dest_lang is None:
                messagebox.showwarning("Language Error", "Invalid target language selected.")
                restore_button()
                return

            translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(source_text)

            text_output.delete("0.0", "end")
            text_output.insert("end", translated)

        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")

        restore_button()


    translate_btn.pack_forget()
    loading_label.pack(pady=15)
    threading.Thread(target=worker, daemon=True).start()


def restore_button():
    loading_label.pack_forget()
    translate_btn.pack(pady=15)


title_label = ctk.CTkLabel(app, text="🌐 Language Translator", font=("Segoe UI", 20, "bold"))
title_label.pack(pady=15)


frame_text = ctk.CTkFrame(app, fg_color="transparent")
frame_text.pack(pady=10)

text_input = ctk.CTkTextbox(frame_text, width=380, height=250, corner_radius=15, font=FONT_MAIN)
text_input.grid(row=0, column=0, padx=20)

text_output = ctk.CTkTextbox(frame_text, width=380, height=250, corner_radius=15, font=FONT_MAIN)
text_output.grid(row=0, column=1, padx=20)


frame_lang = ctk.CTkFrame(app, fg_color="transparent")
frame_lang.pack(pady=10)

combo_source = ctk.CTkComboBox(frame_lang, values=lang_names, width=250, font=FONT_MAIN, state="normal")
combo_source.grid(row=0, column=0, padx=20)
combo_source.set("auto (detect)")

combo_target = ctk.CTkComboBox(frame_lang, values=lang_names[1:], width=250, font=FONT_MAIN, state="normal")
combo_target.grid(row=0, column=1, padx=20)
combo_target.set("english")


translate_btn = ctk.CTkButton(app, text="Translate", font=FONT_BOLD, command=translate_text, width=200, corner_radius=12)
translate_btn.pack(pady=15)

loading_label = ctk.CTkLabel(app, text="⏳ Translating...", font=FONT_BOLD)



app.mainloop()
