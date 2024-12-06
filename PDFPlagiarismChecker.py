#References:
#PDFphraseSearch
#Campus Navigation Project
#Refeference/debugging tool: ChatGPT


#GUI imports
import tkinter as tk
from tkinter import messagebox
import fitz
from tkinter import filedialog
import os

#Creating main window
root = tk.Tk()
root.title("PDF Plagiarism Checker")
root.geometry("600x500")
root.configure(bg="#ADD8E6")

#Functions
def get_text(pdf, count):
    text = ""
    for i in range(count):
        page = pdf.load_page(i)
        text += page.get_text()
    return text

def get_master_pdf():
    global pdf_path
    global master_file_name
    global master_pdf
    global master_pdf_text

    pdf_path = filedialog.askopenfilename()

    master_file_name = os.path.basename(pdf_path)
    master_pdf = fitz.open(pdf_path)
    pg_count = master_pdf.page_count
    master_pdf_text = get_text(master_pdf, pg_count)

    label_2.config(text=master_file_name)
    master_pdf.close()

def get_pattern_pdf():
    global pdf_path
    global pattern_file_name
    global pattern_pdf
    global pattern_pdf_text

    pdf_path = filedialog.askopenfilename()

    pattern_file_name = os.path.basename(pdf_path)
    pattern_pdf = fitz.open(pdf_path)
    pg_count = pattern_pdf.page_count
    pattern_pdf_text = get_text(pattern_pdf, pg_count)

    label_4.config(text=pattern_file_name)
    pattern_pdf.close()
    
def get_result():
    global master_pdf_text
    global pattern_pdf_text

    if master_pdf_text == "":
        messagebox.showerror("Error", "Please enter a valid Master file!")
    elif pattern_pdf_text == "":
        messagebox.showerror("Error", "Please enter a valid Pattern file!")
    else:
        display(master_pdf_text, pattern_pdf_text)
        
def pair_split(pattern):
    intt = 0
    words = pattern.split()
    sections = []
    for i in range(0, len(words)-1, 2):
        sections.append(words[i]+ " " + words[i+1])  
    
    return sections

def compute_prefix_table(pattern):
    prefix_table = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = prefix_table[j-1]
            if pattern[i] == pattern[j]:
                j+=1
            prefix_table[i] = j
    return prefix_table

def kmp_search(text, pattern):
    visited = []
    prefix_table = compute_prefix_table(pattern)
    i = j = 0
    count = 0
    if pattern not in visited:
        visited.append(pattern)
        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1
                if j == len(pattern):
                    count += 1
                    j = prefix_table[j -1]

            else:
                if j >0 :
                    j = prefix_table[j-1]
                else:
                    i+=1
    return (count * len(pattern))

def match_percentage(text, pattern):
    sections = pair_split(pattern)
    matched_chars = 0
    for i in range(len(sections)-1):
        matched_chars += kmp_search(text, sections[i])
    if matched_chars > len(pattern):
        mismatch = (matched_chars - len(pattern))
        matched_chars - mismatch
    elif len(pattern) > matched_chars:
        mismatch = (len(pattern) - matched_chars)
        matched_chars + mismatch

    if (len(text) >= len(pattern)):
        percentage = (matched_chars/len(text))*100
    elif (len(text) < len(pattern)):
        percentage = (len(text)/matched_chars)*100
    
    return percentage

def display(text, pattern):
    match_percent = match_percentage(text, pattern)
    if match_percent < 50.0:
        result = f"The plagiarism percentage is {match_percent:.2f}%\nLikelihood of plagiarism is low."
        print(result)
        messagebox.showinfo("Information", result)
    if match_percent >= 50.0:
        result = f"The plagiarism percentage is {match_percent:.2f}%\nLikelihood of plagiarism is high."
        print(result)
        messagebox.showinfo("Information", result)





#Variables
pdf_path = ""
master_file_name = ""
pattern_file_name = ""
master_pdf = None
pattern_pdf = None
master_pdf_text = ""
pattern_pdf_text = ""



# UI
#Master file label
label_1 = tk.Label(root, text="Master File", font = ("Arial",16, "bold"), fg="#547B91", bg= "#ADD8E6")
label_1.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="e")

#Upload button
uploadButton_1 = tk.Button(root, text="Upload", font=("Arial",14 ,"bold"), fg="white", bg="#6A8DAD", command=get_master_pdf)
uploadButton_1.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

#File name printout
label_2 = tk.Label(root, text=master_file_name, font = ("Arial",14, "bold"), fg="#6A8DAD", bg= "#ADD8E6")
label_2.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="e")

#Pattern file label
label_3 = tk.Label(root, text="Pattern File", font = ("Arial",16, "bold"), fg="#547B91", bg= "#ADD8E6")
label_3.grid(row=2, column=2, columnspan=1, padx=10, pady=10, sticky="e")

#Upload button
uploadButton_2 = tk.Button(root, text="Upload", font=("Arial",14 ,"bold"), fg="white", bg="#6A8DAD", command=get_pattern_pdf)
uploadButton_2.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

#File name printout
label_4 = tk.Label(root, text=pattern_file_name, font = ("Arial",14, "bold"), fg="#6A8DAD", bg= "#ADD8E6")
label_4.grid(row=3, column=2, columnspan=1, padx=10, pady=10, sticky="e")

#Submit Button
subButton = tk.Button(root, text="Check", font=("Arial",14 ,"bold"), fg="white", bg="#547B91", command=get_result)
subButton.grid(row=4, column=1, columnspan=3, pady=10)



#Configuring grid columns
root.grid_columnconfigure(0, weight=0, minsize=150)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=0, minsize=50)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=0, minsize=50)
root.grid_columnconfigure(5, weight=1)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

#Event Loop
root.mainloop()
