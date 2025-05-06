import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def split_pdf(input_pdf_path, pages_per_split, output_folder, progress_var):
    pdf_document = fitz.open(input_pdf_path)
    total_pages = pdf_document.page_count
    num_splits = (total_pages + pages_per_split - 1) // pages_per_split

    processed_pages = 0

    for i in range(num_splits):
        start_page = i * pages_per_split
        end_page = min(start_page + pages_per_split, total_pages)
        split_pdf = fitz.open()

        for page_num in range(start_page, end_page):
            split_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            processed_pages += 1
            progress = (processed_pages / total_pages) * 100
            progress_var.set(progress)
            root.update_idletasks()

        output_filename = f"{output_folder}/split_{i + 1}.pdf"
        split_pdf.save(output_filename)
        split_pdf.close()

    pdf_document.close()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

def show_total_pages():
    input_pdf_path = file_entry.get()
    if not input_pdf_path:
        messagebox.showerror("Input Error", "Please select a PDF file.")
        return

    pdf_document = fitz.open(input_pdf_path)
    total_pages = pdf_document.page_count
    pdf_document.close()

    messagebox.showinfo("Total Pages", f"The selected PDF has {total_pages} pages.")

def split_pdf_gui():
    input_pdf_path = file_entry.get()
    output_folder = output_entry.get()
    try:
        pages_per_split = int(pages_entry.get())
        if pages_per_split <= 0:
            raise ValueError("Number of pages per split must be greater than 0.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return

    if not input_pdf_path:
        messagebox.showerror("Input Error", "Please select a PDF file.")
        return

    if not output_folder:
        messagebox.showerror("Output Error", "Please select an output folder.")
        return

    progress_var.set(0)

    # Run the splitting in a separate thread
    threading.Thread(
        target=split_pdf,
        args=(input_pdf_path, pages_per_split, output_folder, progress_var),
        daemon=True
    ).start()


# GUI setup
root = tk.Tk()
root.title("PDF Splitter")

tk.Label(root, text="Select PDF file:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select output folder:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Pages per split:").grid(row=2, column=0, padx=10, pady=10)
pages_entry = tk.Entry(root, width=10)
pages_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Show Total Pages", command=show_total_pages).grid(row=3, column=0, columnspan=3, pady=10)
tk.Button(root, text="Split PDF", command=split_pdf_gui).grid(row=4, column=0, columnspan=3, pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

root.mainloop()
