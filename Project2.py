import tkinter as tk
from tkinter import messagebox
import json

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f0f0")

        self.bg_color = "#4CAF50"
        self.button_color = "#FF9800"
        self.active_button_color = "#FF5722"
        self.label_color = "#2196F3"

        self.score = 0
        self.question_index = 0
        self.timer = 10
        self.questions = {}
        self.selected_category = ""
        self.timer_id = None  # To store the reference to the timer update

        self.load_questions()
        self.show_main_menu()

    def load_questions(self):
        try:
            with open("questions.json", "r") as file:
                self.questions = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading questions: {e}")
            self.root.quit()

    def show_main_menu(self):
        self.clear_screen()

        quiz_frame = tk.Frame(self.root, bg=self.bg_color, bd=5, relief="solid", width=500, height=350)
        quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.category_label = tk.Label(quiz_frame, text="Select your Quiz choice", font=("Arial", 24, "bold"), bg=self.bg_color, fg="white", width=30, height=3)
        self.category_label.pack(pady=40)

        for category in self.questions.keys():
            button = tk.Button(quiz_frame, text=category, font=("Arial", 16), bg=self.button_color, fg="white", activebackground=self.active_button_color, relief="raised", width=30, height=2,
            command=lambda cat=category: self.start_quiz(cat))
            button.pack(pady=15)

    def start_quiz(self, category):
        self.selected_category = category
        self.score = 0
        self.question_index = 0
        self.timer = 10  # Reset timer when starting a new quiz
        self.display_question()

    def display_question(self):
        if self.question_index >= len(self.questions[self.selected_category]):
            self.end_game()
            return

        self.clear_screen()

        quiz_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid", width=500, height=350)
        quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        question_data = self.questions[self.selected_category][self.question_index]
        question = question_data["question"]
        options = question_data["options"]

        self.question_label = tk.Label(quiz_frame, text=question, font=("Arial", 18, "bold"), bg=self.label_color, fg="white", wraplength=450, relief="solid", padx=20, pady=20)
        self.question_label.pack(pady=30)

        for i, option in enumerate(options):
            button = tk.Button(quiz_frame, text=option, font=("Arial", 14), bg=self.bg_color, fg="white", 
                               activebackground=self.button_color, relief="raised", width=30, height=2,
                               command=lambda i=i: self.check_answer(i))
            button.pack(pady=10)

        self.timer_label = tk.Label(quiz_frame, text=f"Time: {self.timer}s", font=("Arial", 14, "bold"), bg="#FFEB3B", width=20, height=2)
        self.timer_label.pack(pady=10)

        self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}s")
            self.timer_id = self.root.after(1000, self.update_timer)  # Store the timer reference
        else:
            self.timer = 10  # Reset timer after the current question times out
            self.question_index += 1
            self.display_question()

    def check_answer(self, selected_index):
        question_data = self.questions[self.selected_category][self.question_index]
        if question_data["options"][selected_index] == question_data["answer"]:
            self.score += 10

        self.timer = 10  # Reset the timer immediately after answering
        self.question_index += 1

        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)  # Cancel the ongoing timer update

        self.display_question()

    def end_game(self):
        self.clear_screen()

        result_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid", width=500, height=350)
        result_frame.place(relx=0.5, rely=0.5, anchor="center")

        result_label = tk.Label(result_frame, text=f"Your Final Score is: {self.score}  out of 50", font=("Arial", 20, "bold"), bg=self.label_color, fg="white", width=50, height=2)
        result_label.pack(pady=30)

        try_again_button = tk.Button(result_frame, text="Try Again", font=("Arial", 16), bg=self.bg_color, fg="white", activebackground=self.button_color, relief="raised", width=20, height=2, 
        command=lambda: self.start_quiz(self.selected_category))
        try_again_button.pack(pady=20)

        home_button = tk.Button(result_frame, text="Return to Home", font=("Arial", 16), bg=self.button_color, fg="white", activebackground=self.active_button_color, relief="raised", width=20, height=2, command=self.show_main_menu)
        home_button.pack(pady=20)

        exit_button = tk.Button(result_frame, text="Exit", font=("Arial", 16), bg="#f44336", fg="white", relief="raised", width=20, height=2, command=self.exit_game)
        exit_button.pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_game(self):
        self.root.quit()  # Close the application


if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()