import tkinter as tk
from tkinter import messagebox, ttk


class MovieOrganizer:
    def __init__(self):
        self.movies = []  # [(name, rating)]

    # --- DSA Functions ---
    def linear_search(self, name):
        for i in range(len(self.movies)):
            if self.movies[i][0].lower() == name.lower():
                return i
        return -1

    def selection_sort_by_name(self):
        n = len(self.movies)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.movies[j][0].lower() < self.movies[min_idx][0].lower():
                    min_idx = j
            self.movies[i], self.movies[min_idx] = self.movies[min_idx], self.movies[i]

    def selection_sort_by_rating(self):
        n = len(self.movies)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.movies[j][1] < self.movies[min_idx][1]:
                    min_idx = j
            self.movies[i], self.movies[min_idx] = self.movies[min_idx], self.movies[i]

    # --- Data Operations ---
    def add_movie(self, name, rating):
        self.movies.append((name, rating))

    def delete_movie(self, name):
        idx = self.linear_search(name)
        if idx != -1:
            del self.movies[idx]
            return True
        return False


# ----------------------------------------------------------
# GUI Application
# ----------------------------------------------------------
class MovieGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Rating Organizer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.organizer = MovieOrganizer()

        # --- Title ---
        tk.Label(root, text="🎞️ Movie Rating Organizer", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Input Frame ---
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Movie Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame, width=25, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Rating (0–10):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(frame, width=25, font=("Arial", 12))
        self.rating_entry.grid(row=1, column=1, padx=5)

        tk.Button(frame, text="Add Movie", command=self.add_movie, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, rowspan=2, padx=10)

        # --- TreeView Table ---
        self.tree = ttk.Treeview(root, columns=("Name", "Rating"), show='headings', height=12)
        self.tree.heading("Name", text="Movie Name")
        self.tree.heading("Rating", text="Rating")
        self.tree.column("Name", width=300)
        self.tree.column("Rating", width=100)
        self.tree.pack(pady=10)

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Sort by Name", command=self.sort_by_name, width=15, bg="#2196F3", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sort by Rating", command=self.sort_by_rating, width=15, bg="#673AB7", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Search Movie", command=self.search_movie, width=15, bg="#FF9800", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Delete Movie", command=self.delete_movie, width=15, bg="#F44336", fg="white").grid(row=0, column=3, padx=5)

    # --- Helper Functions ---
    def add_movie(self):
        name = self.name_entry.get().strip()
        rating_text = self.rating_entry.get().strip()

        if not name or not rating_text:
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return

        try:
            rating = float(rating_text)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Rating must be a number between 0 and 10.")
            return

        self.organizer.add_movie(name, rating)
        self.refresh_table()
        self.name_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a movie to delete.")
            return

        name = self.tree.item(selected[0])['values'][0]
        if self.organizer.delete_movie(name):
            self.refresh_table()
            messagebox.showinfo("Deleted", f"'{name}' removed successfully.")
        else:
            messagebox.showerror("Error", "Movie not found.")

    def sort_by_name(self):
        self.organizer.selection_sort_by_name()
        self.refresh_table()

    def sort_by_rating(self):
        self.organizer.selection_sort_by_rating()
        self.refresh_table()

    def search_movie(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Enter a movie name to search.")
            return

        idx = self.organizer.linear_search(name)
        if idx != -1:
            messagebox.showinfo("Movie Found", f"'{self.organizer.movies[idx][0]}' found with rating {self.organizer.movies[idx][1]}")
        else:
            messagebox.showinfo("Not Found", "Movie not found in the list.")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for movie in self.organizer.movies:
            self.tree.insert("", tk.END, values=movie)


# ----------------------------------------------------------
# Run GUI
# ----------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieGUI(root)
    root.mainloop()
