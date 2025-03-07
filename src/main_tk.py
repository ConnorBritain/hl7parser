#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from parser.hl7_parser import HL7Parser

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.parser = HL7Parser()
        self.init_ui()
        
    def init_ui(self):
        self.root.title("HL7 Parser (Tkinter Version)")
        self.root.geometry("1200x800")
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window (like splitter)
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(paned, text="Enter or paste HL7 message:")
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.parse_button = ttk.Button(button_frame, text="Parse Message", command=self.parse_input_text)
        self.parse_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(paned, text="Parsed Message Structure:")
        
        # Create Treeview for displaying parsed data
        tree_frame = ttk.Frame(output_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Element", "Value"), show="headings")
        self.tree.heading("Element", text="Element")
        self.tree.heading("Value", text="Value")
        self.tree.column("Element", width=300)
        self.tree.column("Value", width=500)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Export buttons
        export_frame = ttk.Frame(output_frame)
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.copy_button = ttk.Button(export_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(export_frame, text="Export to File", command=self.export_to_file)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        # Add frames to paned window
        paned.add(input_frame, weight=1)
        paned.add(output_frame, weight=2)
    
    def parse_input_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter an HL7 message to parse.")
            return
        
        try:
            self.parser.parse_text(text)
            self.display_message_structure()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Open HL7 File",
            filetypes=[("HL7 Files", "*.hl7"), ("All Files", "*")]
        )
        
        if not file_path:
            return
        
        try:
            self.parser.parse_file(file_path)
            with open(file_path, 'r') as f:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", f.read())
            self.display_message_structure()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def display_message_structure(self):
        # Clear current tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        structure = self.parser.get_structure()
        if not structure:
            return
        
        # Add root item
        root_id = self.tree.insert("", "end", text=structure['name'], 
                                  values=(structure['name'], structure['value'] or ""))
        
        # Populate with children
        self.populate_tree(root_id, structure['children'])
        
        # Expand root
        self.tree.item(root_id, open=True)
    
    def populate_tree(self, parent_id, children):
        for child in children:
            child_id = self.tree.insert(parent_id, "end", text=child['name'],
                                     values=(child['name'], child['value'] or ""))
            
            if child['children']:
                self.populate_tree(child_id, child['children'])
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def copy_to_clipboard(self):
        if not hasattr(self.parser, 'message') or not self.parser.message:
            messagebox.showwarning("Warning", "No parsed message to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(str(self.parser.message))
        
        messagebox.showinfo(
            "Privacy Warning", 
            "The parsed message has been copied to your clipboard. "
            "Remember that this data may contain PHI. "
            "Paste it only in secure locations and clear your clipboard when done."
        )
    
    def export_to_file(self):
        if not hasattr(self.parser, 'message') or not self.parser.message:
            messagebox.showwarning("Warning", "No parsed message to export.")
            return
        
        confirmation = messagebox.askyesno(
            "Privacy Warning",
            "Exporting will save PHI to disk. Only do this if necessary and secure. Continue?"
        )
        
        if not confirmation:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Parsed Message",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as f:
                f.write(str(self.parser.message))
            
            messagebox.showinfo(
                "Export Complete",
                f"Message exported to {file_path}. Please delete this file when no longer needed."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()