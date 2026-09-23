import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.analyzer import analyze_password
from src.pattern_checker import check_password_patterns
from src.wordlist_generator import generate_wordlist, export_wordlist


# -----------------------------
# Colour settings
# -----------------------------
BG_COLOR = "#F3F6FA"
ACCENT_COLOR = "#173B57"
TEXT_COLOR = "#263746"


class PasswordAnalyzerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("PwdScope")
        self.root.geometry("900x760")
        self.root.minsize(650, 600)
        self.root.configure(bg=BG_COLOR)

        # Password analyzer variables
        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar(value=False)
        self.personalized_var = tk.BooleanVar(value=False)

        self.name_var = tk.StringVar()
        self.pet_var = tk.StringVar()
        self.year_var = tk.StringVar()

        # Wordlist generator variables
        self.gen_name_var = tk.StringVar()
        self.gen_pet_var = tk.StringVar()
        self.gen_year_var = tk.StringVar()
        self.gen_phrase_var = tk.StringVar()
        self.max_items_var = tk.StringVar(value="200")

        self.setup_styles()
        self.build_interface()

    # ==========================================
    # STYLE SETTINGS
    # ==========================================

    def setup_styles(self):

        style = ttk.Style()

        style.configure(
            "TFrame",
            background=BG_COLOR
        )

        style.configure(
            "TLabel",
            background=BG_COLOR,
            foreground=TEXT_COLOR
        )

        style.configure(
            "Title.TLabel",
            font=("Georgia", 22, "bold"),
            foreground=ACCENT_COLOR
        )

        style.configure(
            "Heading.TLabel",
            font=("Segoe UI", 15, "bold"),
            foreground=ACCENT_COLOR
        )

        style.configure(
            "TNotebook",
            background=BG_COLOR
        )

        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8)
        )

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    # ==========================================
    # MAIN INTERFACE
    # ==========================================

    def build_interface(self):

        main_frame = ttk.Frame(
            self.root,
            padding=20
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        # Main heading
        ttk.Label(
            main_frame,
            text="PwdScope",
            style="Title.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        ttk.Label(
            main_frame,
            text="Password strength analysis & custom wordlist generation"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # Create tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(
            fill="both",
            expand=True
        )

        self.analyzer_tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.generator_tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            self.analyzer_tab,
            text="Password Analyzer"
        )

        self.notebook.add(
            self.generator_tab,
            text="Wordlist Generator"
        )

        self.build_analyzer_tab()
        self.build_generator_tab()

    # ==========================================
    # PASSWORD ANALYZER TAB
    # ==========================================

    def build_analyzer_tab(self):

        tab = self.analyzer_tab

        ttk.Label(
            tab,
            text="Analyze Password Strength",
            style="Heading.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        ttk.Label(
            tab,
            text="Enter a sample password:"
        ).pack(anchor="w")

        # Password entry and show-password checkbox
        password_frame = ttk.Frame(tab)
        password_frame.pack(
            fill="x",
            pady=6
        )

        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            font=("Segoe UI", 11)
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Checkbutton(
            password_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(
            side="left",
            padx=(10, 0)
        )

        # Personal context checkbox
        ttk.Checkbutton(
            tab,
            text="Use personal context",
            variable=self.personalized_var,
            command=self.toggle_personal_fields
        ).pack(
            anchor="w",
            pady=8
        )

        # Optional personal context fields
        self.personal_frame = ttk.LabelFrame(
            tab,
            text="Personal Context (Optional)",
            padding=10
        )

        self.add_field(
            self.personal_frame,
            "Name:",
            self.name_var
        )

        self.add_field(
            self.personal_frame,
            "Pet name:",
            self.pet_var
        )

        self.add_field(
            self.personal_frame,
            "Year:",
            self.year_var
        )

        # Initially hide the personal context fields
        self.personal_frame.pack_forget()

        # Analyze button
        self.analyze_button = ttk.Button(
            tab,
            text="Analyze Password",
            command=self.analyze,
            style="Accent.TButton"
        )

        self.analyze_button.pack(
            anchor="w",
            pady=10
        )

        ttk.Separator(tab).pack(
            fill="x",
            pady=8
        )

        # Analysis results heading
        ttk.Label(
            tab,
            text="Analysis Results",
            style="Heading.TLabel"
        ).pack(anchor="w")

        results_frame = ttk.Frame(tab)
        results_frame.pack(
            fill="both",
            expand=True,
            pady=8
        )

        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical"
        )

        self.results = tk.Text(
            results_frame,
            height=12,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 10),
            bg="white",
            fg=TEXT_COLOR,
            yscrollcommand=scrollbar.set,
            padx=8,
            pady=8
        )

        scrollbar.config(
            command=self.results.yview
        )

        self.results.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ==========================================
    # WORDLIST GENERATOR TAB
    # ==========================================

    def build_generator_tab(self):

        tab = self.generator_tab

        ttk.Label(
            tab,
            text="Custom Wordlist Generator",
            style="Heading.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        ttk.Label(
            tab,
            text=(
                "Enter sample details to generate "
                "password variations:"
            ),
            wraplength=620
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        form_frame = ttk.Frame(
    tab,
    padding=12
)

        form_frame.pack(
            fill="x",
            pady=5
        )

        self.add_field(
            form_frame,
            "Name:",
            self.gen_name_var
        )

        self.add_field(
            form_frame,
            "Pet name:",
            self.gen_pet_var
        )

        self.add_field(
            form_frame,
            "Year:",
            self.gen_year_var
        )

        self.add_field(
            form_frame,
            "Phrase:",
            self.gen_phrase_var
        )

        self.add_field(
            form_frame,
            "Max items:",
            self.max_items_var
        )

        ttk.Label(
            tab,
            text=(
                "Use fictional details for testing "
            
            ),
            wraplength=620
        ).pack(
            anchor="w",
            pady=8
        )

        ttk.Button(
            tab,
            text="Generate and Save Wordlist",
            command=self.generate,
            style="Accent.TButton"
        ).pack(
            anchor="w",
            pady=10
        )

        ttk.Separator(tab).pack(
            fill="x",
            pady=8
        )

        ttk.Label(
            tab,
            text="Generation Status",
            style="Heading.TLabel"
        ).pack(anchor="w")

        self.generator_status = tk.Text(
            tab,
            height=8,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 10),
            bg="white",
            fg=TEXT_COLOR,
            padx=8,
            pady=8
        )

        self.generator_status.pack(
            fill="both",
            expand=True,
            pady=8
        )

        self.update_generator_status(
            "Your wordlist generation status will appear here."
        )

    # ==========================================
    # REUSABLE INPUT FIELD
    # ==========================================

    def add_field(self, parent, label_text, variable):

        row = ttk.Frame(parent)
        row.pack(
            fill="x",
            pady=4
        )

        ttk.Label(
            row,
            text=label_text,
            width=12
        ).pack(side="left")

        ttk.Entry(
            row,
            textvariable=variable
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # ==========================================
    # PASSWORD ANALYZER FUNCTIONS
    # ==========================================

    def toggle_password(self):

        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def toggle_personal_fields(self):

        if self.personalized_var.get():

            # Show the fields directly before the Analyze button
            self.personal_frame.pack(
                before=self.analyze_button,
                fill="x",
                pady=5
            )

        else:
            self.personal_frame.pack_forget()

    def analyze(self):

        password = self.password_var.get()

        if not password:
            messagebox.showwarning(
                "Missing Password",
                "Please enter a sample password."
            )
            return

        personal_terms = []

        # Only include personal details when checkbox is selected
        if self.personalized_var.get():

            personal_terms = [
                self.name_var.get().strip(),
                self.pet_var.get().strip(),
                self.year_var.get().strip()
            ]

            personal_terms = [
                term for term in personal_terms if term
            ]

        try:

            result = analyze_password(
                password,
                personal_terms=personal_terms
            )

            findings = check_password_patterns(
                password,
                personal_terms=personal_terms
            )

            output = [
                "--- Password Analysis ---",
                f"Estimated score: {result['score']}/4",
                f"Estimated category: {result['strength']}",
                ""
            ]

            if result["warning"]:
                output.append(
                    f"Warning: {result['warning']}"
                )
                output.append("")

            output.append("zxcvbn Suggestions:")

            if result["suggestions"]:

                for suggestion in result["suggestions"]:
                    output.append(f"- {suggestion}")

            else:
                output.append(
                    "- No additional suggestions."
                )

            output.append("")
            output.append("Pattern Checks:")

            if findings:

                for item in findings:
                    output.append(
                        f"- {item['finding']}"
                    )

                    output.append(
                        f"  Advice: {item['advice']}"
                    )

            else:
                output.append(
                    "- No listed patterns detected."
                )

            output.extend([
                "",
                "Note: Results are estimates and do not "
                "guarantee password security."
            ])

            # Display results
            self.results.configure(state="normal")

            self.results.delete(
                "1.0",
                "end"
            )

            self.results.insert(
                "1.0",
                "\n".join(output)
            )

            self.results.configure(state="disabled")

        except ValueError as error:

            messagebox.showerror(
                "Input Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Analysis Error",
                str(error)
            )

    # ==========================================
    # WORDLIST GENERATOR FUNCTIONS
    # ==========================================

    def update_generator_status(self, text):

        self.generator_status.configure(
            state="normal"
        )

        self.generator_status.delete(
            "1.0",
            "end"
        )

        self.generator_status.insert(
            "1.0",
            text
        )

        self.generator_status.configure(
            state="disabled"
        )

    def generate(self):

        try:

            # Validate maximum number of candidates
            max_items = int(
                self.max_items_var.get()
            )

            if max_items < 1 or max_items > 5000:
                raise ValueError(
                    "Max items must be between 1 and 5000."
                )

            # Generate candidates using the existing module
            candidates = generate_wordlist(
                name=self.gen_name_var.get(),
                pet=self.gen_pet_var.get(),
                year=self.gen_year_var.get(),
                phrase=self.gen_phrase_var.get(),
                max_items=max_items
            )

            if not candidates:

                messagebox.showinfo(
                    "No Candidates",
                    "Please enter some sample details first."
                )
                return

            # Ask where to save the text file
            output_file = filedialog.asksaveasfilename(
                title="Save Custom Wordlist",
                defaultextension=".txt",
                initialfile="custom_wordlist.txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )

            # User cancelled the save dialog
            if not output_file:
                return

            # Export using the existing function
            saved_path = export_wordlist(
                candidates,
                output_file
            )

            status = (
                "Wordlist generated successfully!\n\n"
                f"Candidates created: {len(candidates)}\n"
                f"Saved file: {saved_path}\n\n"
                "Use generated lists only for authorized "
                "learning and security testing."
            )

            self.update_generator_status(status)

            messagebox.showinfo(
                "Success",
                f"Wordlist saved successfully!\n\n{saved_path}"
            )

        except ValueError as error:

            messagebox.showwarning(
                "Input Error",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Generation Error",
                str(error)
            )


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

def main():

    root = tk.Tk()
    PasswordAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()