import sys
import csv
from PyQt5.QtWidgets import *

# Global variables for data storage
rentals_data = []
equipment_data = []
clients_data = []

# Function to read data from CSV files
def read_data_from_csv():
    global rentals_data, equipment_data, clients_data
    try:
        with open('rentals.csv', newline='', encoding='utf-8') as csvfile:
            rentals_reader = csv.DictReader(csvfile)
            rentals_data = [row for row in rentals_reader]

        with open('equipment.csv', newline='', encoding='utf-8') as csvfile:
            equipment_reader = csv.DictReader(csvfile)
            equipment_data = [row for row in equipment_reader]

        with open('clients.csv', newline='', encoding='utf-8') as csvfile:
            clients_reader = csv.DictReader(csvfile)
            clients_data = [row for row in clients_reader]
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        sys.exit(1)

# Function to write data to CSV files
def write_data_to_csv():
    global rentals_data, equipment_data, clients_data
    try:
        with open('rentals.csv', 'w', newline='', encoding='utf-8') as csvfile:
            rentals_writer = csv.DictWriter(csvfile, fieldnames=rentals_data[0].keys())
            rentals_writer.writeheader()
            rentals_writer.writerows(rentals_data)

        with open('equipment.csv', 'w', newline='', encoding='utf-8') as csvfile:
            equipment_writer = csv.DictWriter(csvfile, fieldnames=equipment_data[0].keys())
            equipment_writer.writeheader()
            equipment_writer.writerows(equipment_data)

        with open('clients.csv', 'w', newline='', encoding='utf-8') as csvfile:
            clients_writer = csv.DictWriter(csvfile, fieldnames=clients_data[0].keys())
            clients_writer.writeheader()
            clients_writer.writerows(clients_data)
    except Exception as e:
        print(f"Error writing CSV files: {e}")
        sys.exit(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equipment Rental System")
        self.initUI()
        read_data_from_csv()  # Read initial data from CSV files

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create layout
        self.layout = QVBoxLayout(self.central_widget)

        # Add buttons for actions
        self.add_equipment_button = QPushButton("Add Equipment")
        self.add_equipment_button.clicked.connect(self.add_equipment_dialog)
        self.layout.addWidget(self.add_equipment_button)

        self.delete_equipment_button = QPushButton("Delete Equipment")
        self.delete_equipment_button.clicked.connect(self.delete_equipment)
        self.layout.addWidget(self.delete_equipment_button)

        self.add_client_button = QPushButton("Add New Client")
        self.add_client_button.clicked.connect(self.add_client_dialog)
        self.layout.addWidget(self.add_client_button)

        self.display_equipment_button = QPushButton("Display Equipment")
        self.display_equipment_button.clicked.connect(self.display_equipment)
        self.layout.addWidget(self.display_equipment_button)

        self.display_clients_button = QPushButton("Display All Clients")
        self.display_clients_button.clicked.connect(self.display_clients)
        self.layout.addWidget(self.display_clients_button)

        self.process_rental_button = QPushButton("Process Rental")
        self.process_rental_button.clicked.connect(self.process_rental)
        self.layout.addWidget(self.process_rental_button)

    def add_equipment_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Equipment")
        layout = QFormLayout()

        id_edit = QLineEdit()
        category_edit = QLineEdit()
        name_edit = QLineEdit()
        description_edit = QLineEdit()
        daily_rental_cost_edit = QLineEdit()

        layout.addRow("ID:", id_edit)
        layout.addRow("Category:", category_edit)
        layout.addRow("Name:", name_edit)
        layout.addRow("Description:", description_edit)
        layout.addRow("Daily Rental Cost:", daily_rental_cost_edit)

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_equipment(id_edit.text(), category_edit.text(), name_edit.text(), description_edit.text(), daily_rental_cost_edit.text(), dialog))
        layout.addWidget(add_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_equipment(self, id, category, name, description, daily_rental_cost, dialog):
        new_equipment = {'id': id, 'category': category, 'name': name, 'description': description, 'daily_rental_cost': daily_rental_cost}
        equipment_data.append(new_equipment)
        write_data_to_csv()
        self.display_equipment()
        dialog.close()

    def delete_equipment(self):
        if equipment_data:
            equipment_data.pop()
            write_data_to_csv()
            self.display_equipment()
        else:
            QMessageBox.warning(self, "Warning", "No equipment to delete.")

    def add_client_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Client")
        layout = QFormLayout()

        customer_id_edit = QLineEdit()
        last_name_edit = QLineEdit()
        first_name_edit = QLineEdit()
        contact_phone_edit = QLineEdit()
        email_edit = QLineEdit()

        layout.addRow("Customer ID:", customer_id_edit)
        layout.addRow("Last Name:", last_name_edit)
        layout.addRow("First Name:", first_name_edit)
        layout.addRow("Contact Phone:", contact_phone_edit)
        layout.addRow("Email:", email_edit)

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_client(customer_id_edit.text(), last_name_edit.text(), first_name_edit.text(), contact_phone_edit.text(), email_edit.text(), dialog))
        layout.addWidget(add_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_client(self, customer_id, last_name, first_name, contact_phone, email, dialog):
        new_client = {'customer_id': customer_id, 'last_name': last_name, 'first_name': first_name, 'contact_phone': contact_phone, 'email': email}
        clients_data.append(new_client)
        write_data_to_csv()
        self.display_clients()
        dialog.close()

    def display_equipment(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Equipment List")
        layout = QVBoxLayout()
        equipment_text_edit = QTextEdit()
        equipment_text_edit.setPlainText("\n".join(','.join(row.values()) for row in equipment_data))
        layout.addWidget(equipment_text_edit)
        dialog.setLayout(layout)
        dialog.exec_()

    def display_clients(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Clients List")
        layout = QVBoxLayout()
        clients_text_edit = QTextEdit()
        clients_text_edit.setPlainText("\n".join(','.join(row.values()) for row in clients_data))
        layout.addWidget(clients_text_edit)
        dialog.setLayout(layout)
        dialog.exec_()

    def process_rental(self):
        self.display_rentals()

    def display_rentals(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("All Rentals")
        layout = QVBoxLayout()
        rentals_text_edit = QTextEdit()
        rentals_text_edit.setPlainText("\n".join(','.join(row.values()) for row in rentals_data))
        layout.addWidget(rentals_text_edit)
        dialog.setLayout(layout)
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# Create and show the main window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
