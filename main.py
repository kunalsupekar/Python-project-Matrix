import tkinter as tk
from fpdf import FPDF

class SeatReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seat Reservation App")

        self.total_rows = 5
        self.total_columns = 6

        self.pre_reserved_seats_matrix = [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0],  # Example pre-reserved seats matrix
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0]
        ]

        self.seat_buttons = []
        self.seat_status = [[0] * self.total_columns for _ in range(self.total_rows)]

        self.create_seating_arrangement()
        self.create_status_bar()
        self.create_submit_button()

    def create_seating_arrangement(self):
        for row in range(self.total_rows):
            self.root.grid_rowconfigure(row, weight=1)
            row_buttons = []
            for col in range(self.total_columns):
                self.root.grid_columnconfigure(col, weight=1)
                seat_number = f"{row + 1}-{col + 1}"
                button = tk.Button(self.root, text=f"Seat {seat_number}",
                                   command=lambda r=row, c=col: self.reserve_seat(r, c, seat_number))
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                if self.pre_reserved_seats_matrix[row][col] == 1:
                    self.seat_status[row][col] = 1
                    button.config(state=tk.DISABLED, bg="light blue", text=f"Pre-Reserved\n{seat_number}")

                row_buttons.append(button)
            self.seat_buttons.append(row_buttons)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=self.total_rows, columnspan=self.total_columns, sticky="we")
        self.update_status_bar()

    def create_submit_button(self):
        self.submit_button = tk.Button(self.root, text="Submit", command=self.generate_report_and_matrix)
        self.submit_button.grid(row=self.total_rows + 1, columnspan=self.total_columns)

    def update_status_bar(self):
        total_seats = self.total_rows * self.total_columns
        reserved_seats = sum(row.count(1) for row in self.seat_status)
        remaining_seats = total_seats - reserved_seats
        self.status_bar.config(
            text=f"Reserved Seats: {reserved_seats} | Total Seats: {total_seats} | Remaining Seats: {remaining_seats}")

    def reserve_seat(self, row, col, seat_number):
        if self.seat_status[row][col] == 0:
            self.seat_status[row][col] = 1
            self.seat_buttons[row][col].config(state=tk.DISABLED, bg="red", text=f"Reserved\n{seat_number}")
        else:
            self.seat_status[row][col] = 0
            self.seat_buttons[row][col].config(state=tk.NORMAL, bg="SystemButtonFace", text=f"Seat {seat_number}")

        self.update_status_bar()

    def generate_report_and_matrix(self):
        self.generate_report_pdf()
        self.display_seat_matrix()

    def generate_report_pdf(self):
        report_filename = "seat_reservation_report.pdf"
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Seat Reservation Report", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Reserved Seats:", ln=True)

        for row_idx, row in enumerate(self.seat_status):
            for col_idx, status in enumerate(row):
                if status == 1:
                    seat_number = f"Seat {row_idx+1}-{col_idx+1}"
                    pdf.cell(200, 10, txt=seat_number, ln=True)

        pdf.output(report_filename)
        print(f"PDF report generated: {report_filename}")

    def display_seat_matrix(self):
        print("Seat Matrix:")
        for row in self.seat_status:
            print(row)

    def run(self):
       # self.root.state('zoomed')
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = SeatReservationApp(root)
    app.run()
