import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is an interpreted, high-level and general-purpose programming language.",
            "To be or not to be, that is the question.",
            "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "Life is what happens when you're busy making other plans."
        ]
        
        self.current_text = ""
        self.start_time = 0
        self.running = False
        
        self.setup_ui()
    
    def setup_ui(self):

        self.title_label = tk.Label(
            self.root, 
            text="Typing Speed Test", 
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=20)

        self.sample_label = tk.Label(
            self.root, 
            text="Click 'Start Test' to begin", 
            font=("Helvetica", 14), 
            wraplength=700,
            justify="left"
        )
        self.sample_label.pack(pady=20)
        
        self.text_input = tk.Text(
            self.root, 
            height=10, 
            width=80, 
            font=("Helvetica", 12),
            wrap=tk.WORD
        )
        self.text_input.pack(pady=10)
        self.text_input.config(state="disabled")

        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=10)
        
        self.time_label = tk.Label(
            stats_frame, 
            text="Time: 0s", 
            font=("Helvetica", 12)
        )
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        self.wpm_label = tk.Label(
            stats_frame, 
            text="WPM: 0", 
            font=("Helvetica", 12)
        )
        self.wpm_label.pack(side=tk.LEFT, padx=20)
        
        self.accuracy_label = tk.Label(
            stats_frame, 
            text="Accuracy: 0%", 
            font=("Helvetica", 12)
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=20)
        

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            buttons_frame, 
            text="Start Test", 
            command=self.start_test,
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(
            buttons_frame, 
            text="Reset", 
            command=self.reset_test,
            font=("Helvetica", 14),
            bg="#f44336",
            fg="white"
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)
        

        self.text_input.bind("<KeyRelease>", self.check_completion)
    
    def start_test(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.current_text = random.choice(self.sample_texts)
            self.sample_label.config(text=self.current_text)
            self.text_input.config(state="normal")
            self.text_input.delete("1.0", tk.END)
            self.start_button.config(state="disabled")
            self.update_timer()
    
    def reset_test(self):
        self.running = False
        self.current_text = ""
        self.sample_label.config(text="Click 'Start Test' to begin")
        self.text_input.delete("1.0", tk.END)
        self.text_input.config(state="disabled")
        self.time_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.start_button.config(state="normal")
    
    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}s")

            typed_text = self.text_input.get("1.0", tk.END).strip()
            words = len(typed_text.split())
            minutes = elapsed_time / 60
            wpm = int(words / minutes) if minutes > 0 else 0
            self.wpm_label.config(text=f"WPM: {wpm}")

            self.root.after(1000, self.update_timer)
    
    def check_completion(self, event):
        if self.running:
            typed_text = self.text_input.get("1.0", tk.END).strip()
            sample_text = self.current_text.strip()

            correct_chars = 0
            min_length = min(len(typed_text), len(sample_text))
            
            for i in range(min_length):
                if typed_text[i] == sample_text[i]:
                    correct_chars += 1
            
            accuracy = (correct_chars / len(sample_text)) * 100 if len(sample_text) > 0 else 0
            self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")

            if typed_text == sample_text:
                self.running = False
                elapsed_time = time.time() - self.start_time
                words = len(sample_text.split())
                wpm = int((words / elapsed_time) * 60)
                
                messagebox.showinfo(
                    "Test Complete",
                    f"Your typing speed: {wpm} WPM\n"
                    f"Accuracy: {accuracy:.1f}%\n"
                    f"Time: {elapsed_time:.1f} seconds"
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

