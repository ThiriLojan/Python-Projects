import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import re
from datetime import datetime

# Define the color palette
BG_COLOR = "#000000"            # Light Teal for background
PRIMARY_COLOR = "#3d3d3d"        # Teal for primary accents
HOVER_COLOR = "#20B2AA"          # Light Sea Green for hover effect
SECONDARY_COLOR = "#FFFFFF"      # Dark Gray for text and secondary accents
TEXT_COLOR = "#FFFFFF"           # White for text on buttons

# Global contact list
contacts = []

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")
        self.root.geometry("385x594+300+200")
        self.root.configure(bg=BG_COLOR)
        
        # Applying a theme
        style = ttk.Style()
        style.theme_use("clam")
        
        # Create the main frame
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Call the function to display the main menu
        self.show_navigation_menu()

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, bg=PRIMARY_COLOR, fg=TEXT_COLOR, relief=tk.FLAT)
        button.bind("<Enter>", lambda e: button.config(bg=HOVER_COLOR))
        button.bind("<Leave>", lambda e: button.config(bg=PRIMARY_COLOR))
        return button

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_navigation_menu(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="MyCallerID", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=20)
        
        self.create_button(self.main_frame, text="Contact Book", command=self.show_main_menu).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Track Number", command=self.show_analyze_number).pack(pady=10,padx=10)
    
    def show_main_menu(self):
        self.clear_frame()
        
        tk.Label(self.main_frame, text="Choose an Operation", bg=BG_COLOR, fg=SECONDARY_COLOR,font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        self.create_button(self.main_frame, text="Add Contact", command=self.show_add_contact).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Remove Contact", command=self.show_remove_contact).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Delete All Contacts", command=self.delete_all_contacts).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Search Contact", command=self.show_search_contact).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Display All Contacts", command=self.display_all_contacts).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Return to Navigation Menu", command=self.show_navigation_menu).pack(pady=10,padx=10)

    def show_add_contact(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Add New Contact", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Input fields for contact details
        tk.Label(self.main_frame, text="Name:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.name_entry = tk.Entry(self.main_frame, width=30)
        self.name_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Number:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.number_entry = tk.Entry(self.main_frame, width=30)
        self.number_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Email:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.email_entry = tk.Entry(self.main_frame, width=30)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Date of Birth (dd/mm/yyyy):", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.dob_entry = tk.Entry(self.main_frame, width=30)
        self.dob_entry.pack(pady=5)
        
        tk.Label(self.main_frame, text="Category (Family/Friend/Work/Others):", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.category_entry = tk.Entry(self.main_frame, width=30)
        self.category_entry.pack(pady=5)

        # Button to add contact
        self.create_button(self.main_frame, text="Add Contact", command=self.add_contact).pack(pady=20)
        self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=10)
    
    def add_contact(self):
        name = self.name_entry.get()
        number = self.number_entry.get()
        email = self.email_entry.get()
        dob = self.dob_entry.get()
        category = self.category_entry.get()
        
        if self.validate_input(name, number, email, dob, category):
            contacts.append({"Name": name, "Number": number, "Email": email, "DOB": dob, "Category": category})
            messagebox.showinfo("Info", "Contact added successfully!")
            self.show_main_menu()
        else:
            messagebox.showwarning("Input Error", "Please correct the highlighted fields.")

    def validate_input(self, name, number, email, dob, category):
        valid = True

        # Name validation
        if not name:
            self.highlight_entry(self.name_entry)
            valid = False
        else:
            self.remove_highlight(self.name_entry)
        
        # Phone number validation
        if not self.validate_phone_number(number):
            self.highlight_entry(self.number_entry)
            valid = False
        else:
            self.remove_highlight(self.number_entry)

        # Email validation
        if not self.validate_email(email):
            self.highlight_entry(self.email_entry)
            valid = False
        else:
            self.remove_highlight(self.email_entry)

        # Date of Birth validation
        if not self.validate_dob(dob):
            self.highlight_entry(self.dob_entry)
            valid = False
        else:
            self.remove_highlight(self.dob_entry)
        
        # Category validation
        if not category:
            self.highlight_entry(self.category_entry)
            valid = False
        else:
            self.remove_highlight(self.category_entry)

        return valid

    def validate_phone_number(self, number):
        try:
            parsed_number = phonenumbers.parse(number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False

    def validate_email(self, email):
        # Simple regex for validating email format
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def validate_dob(self, dob):
        try:
            datetime.strptime(dob, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def highlight_entry(self, entry):
        entry.config(bg="lightcoral")

    def remove_highlight(self, entry):
        entry.config(bg="white")

    def show_remove_contact(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Remove Contact", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Input fields for removing contact
        tk.Label(self.main_frame, text="Name:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.remove_name_entry = tk.Entry(self.main_frame)
        self.remove_name_entry.pack(pady=5)
        
        self.create_button(self.main_frame, text="Remove Contact", command=self.remove_contact).pack(pady=20)
        self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=10)

    def remove_contact(self):
        name = self.remove_name_entry.get()
        global contacts
        contacts = [contact for contact in contacts if contact["Name"] != name]
        messagebox.showinfo("Info", "Contact removed if it existed.")
        self.show_main_menu()

    def show_search_contact(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Search Contact", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Dropdown to select the search criteria
        tk.Label(self.main_frame, text="Search by:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        criteria_options = ["Name", "Number", "Email", "DOB", "Category"]
        self.search_criteria_combobox = ttk.Combobox(self.main_frame, values=criteria_options, state="readonly")
        self.search_criteria_combobox.pack(pady=5)
        self.search_criteria_combobox.current(0)  # Set the default value
        
        # Input field for search value
        tk.Label(self.main_frame, text="Value:", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
        self.search_value_entry = tk.Entry(self.main_frame, width=30)
        self.search_value_entry.pack(pady=5)
        
        self.create_button(self.main_frame, text="Search", command=self.search_contact).pack(pady=20)
        self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=10)

    def search_contact(self):
        criteria = self.search_criteria_combobox.get()
        value = self.search_value_entry.get()
        
        found_contacts = [contact for contact in contacts if contact[criteria] == value]
        
        if found_contacts:
            result = "\n".join([f"{contact['Name']} - {contact['Number']} - {contact['Email']} - {contact['DOB']} - {contact['Category']}" for contact in found_contacts])
            messagebox.showinfo("Search Results", f"Found contacts:\n{result}")
        else:
            messagebox.showinfo("Search Results", "No contacts found.")

    def display_all_contacts(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="All Contacts", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=10)

        if contacts:
            # Create a Listbox to display contact names
            self.contact_listbox = tk.Listbox(self.main_frame, width=50, height=15, bg=BG_COLOR, fg=SECONDARY_COLOR, font=("Arial", 12))
            self.contact_listbox.pack(pady=10)

            # Populate Listbox with contact names
            for contact in contacts:
                self.contact_listbox.insert(tk.END, contact["Name"])

            # Bind the click event to show contact details
            self.contact_listbox.bind("<<ListboxSelect>>", self.show_contact_details)

            self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=10)

        else:
            tk.Label(self.main_frame, text="No contacts available.", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=10)
            self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=10)

    def show_contact_details(self, event):
        selected_index = self.contact_listbox.curselection()

        if selected_index:
            selected_name = self.contact_listbox.get(selected_index)
            contact = next((c for c in contacts if c["Name"] == selected_name), None)

            if contact:
                self.clear_frame()

                # Display contact details
                tk.Label(self.main_frame, text=f"Name: {contact['Name']}", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14, 'bold')).pack(pady=5)
                tk.Label(self.main_frame, text=f"Number: {contact['Number']}", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
                tk.Label(self.main_frame, text=f"Email: {contact['Email']}", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
                tk.Label(self.main_frame, text=f"DOB: {contact['DOB']}", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
                tk.Label(self.main_frame, text=f"Category: {contact['Category']}", bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=5)

                self.create_button(self.main_frame, text="Return to All Contacts", command=self.display_all_contacts).pack(pady=20)
                self.create_button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu).pack(pady=30)

    def delete_all_contacts(self):
        global contacts
        contacts = []
        messagebox.showinfo("Info", "All contacts have been deleted.")
        self.show_main_menu()

    def show_analyze_number(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Track Number", bg=BG_COLOR, fg=SECONDARY_COLOR, font=('Helvetica', 14,'bold')).pack(pady=10)
        
        # Input field for phone number
        tk.Label(self.main_frame, text="Enter The Phone Number to Track:", bg=BG_COLOR, fg=SECONDARY_COLOR,font=('Helvetica', 10)).pack(pady=5)
        self.number_entry = tk.Entry(self.main_frame,width=30)
        self.number_entry.pack(pady=5)
        
        self.create_button(self.main_frame, text="Track Number", command=self.analyze_number).pack(pady=10,padx=10)
        self.create_button(self.main_frame, text="Return to Navigation Menu", command=self.show_navigation_menu).pack(pady=10,padx=10)

    def analyze_number(self):
        number = self.number_entry.get()
        
        if number:
            try:
                parsed_number = phonenumbers.parse(number)
                location = geocoder.description_for_number(parsed_number, "en")
                carrier_name = carrier.name_for_number(parsed_number, "en")
                timezone_list = timezone.time_zones_for_number(parsed_number)
        
                info = f"Location: {location}\nCarrier: {carrier_name}\nTimezones: {', '.join(timezone_list)}"
                
                self.clear_frame()
                
                text_area = tk.Text(self.main_frame, wrap=tk.WORD, height=15, width=50, font=("Arial", 12, "bold"), bg=BG_COLOR, fg=SECONDARY_COLOR)
                text_area.pack(pady=10)
                
                # Configure the center alignment tag
                text_area.tag_configure("center", justify="center")
                
                # Insert the info text with the center tag applied
                text_area.insert(tk.END, info)
                text_area.tag_add("center", "1.0", "end")
                
                self.create_button(self.main_frame, text="Return to Navigation Menu", command=self.show_navigation_menu).pack(pady=20)
                
            except phonenumbers.NumberParseException:
                messagebox.showerror("Error", "Invalid phone number format.")
                self.show_analyze_number()

# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
     