import tkinter as tk
from tkinter import messagebox
import json
import os

class ToDoList:
    def __init__(self, root, filename):
        self.root = root
        self.filename = filename
        self.tasks = self.load_tasks()

        self.task_number = 1

        self.task_listbox = tk.Listbox(self.root, width=40)
        self.task_listbox.pack(padx=10, pady=10)

        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add task", command=self.add_task)
        self.add_button.pack(padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete task", command=self.delete_task)
        self.delete_button.pack(padx=10, pady=10)

        self.done_button = tk.Button(self.root, text="Mark task as done", command=self.mark_done)
        self.done_button.pack(padx=10, pady=10)

        self.sort_button = tk.Button(self.root, text="Sort tasks", command=self.sort_tasks)
        self.sort_button.pack(padx=10, pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(padx=10, pady=10)

        self.update_listbox()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "done": False})
            self.save_tasks()
            self.update_listbox()
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(task_index)
            del self.tasks[task_index]
            self.save_tasks()
        except IndexError:
            messagebox.showerror("Error", "Select a task to delete.")

    def mark_done(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.tasks[task_index]["done"] = True
            self.save_tasks()
            self.update_listbox()
        except IndexError:
            messagebox.showerror("Error", "Select a task to mark as done.")

    def sort_tasks(self):
        self.tasks.sort(key=lambda x: x["done"])
        self.save_tasks()
        self.update_listbox()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        else:
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file)

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, start=1):
            done = "*" if task["done"] else " "
            self.task_listbox.insert(tk.END, f"{i}. {task['task']} [{done}]")

def main():
    filename = "todo.json"
    root = tk.Tk()
    root.title("To-Do List")
    todo = ToDoList(root, filename)
    root.mainloop()

if __name__ == "__main__":
    main()