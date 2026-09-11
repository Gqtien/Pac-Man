import sys
from tkinter import Tk


def window_example() -> None:
    tk = Tk()
    tk.title("Pac-Man")
    w, h = tk.winfo_screenwidth(), tk.winfo_screenheight()
    tk.geometry(f"{w}x{h}")
    tk.mainloop()


if __name__ == "__main__":
    try:
        window_example()
    except Exception as exc:
        sys.exit(f"Error: {exc}")
