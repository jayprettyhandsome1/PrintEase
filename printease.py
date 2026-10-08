# printease.py - shared Python code for all PrintEase pages.
# PyScript runs these functions when the user clicks, types, changes
# a dropdown, or submits the order form (event-driven programming).

from pyscript import document

# One price list used by the calculator AND the order form.
PRICES = {
    "bw":    {"short": 2, "long": 3, "a4": 3},   # Black & White
    "color": {"short": 5, "long": 5, "a4": 5},   # Colored
}
TYPE_NAMES = {"bw": "Black & White", "color": "Colored"}
SIZE_NAMES = {"short": "Short", "long": "Long", "a4": "A4"}
FILE_TYPES = (".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png")


def read_copies(text):
    """Return the number of copies as a whole number, or None if it is invalid."""
    try:
        copies = int(text)
    except ValueError:        # empty, letters, or decimals like 2.5
        return None
    if copies < 1:            # zero or negative
        return None
    return copies


def get_selected_file():
    """Return the name of the chosen file, or None if nothing is selected."""
    files = document.querySelector("#o-file").files
    if files.length == 0:
        return None
    return files.item(0).name


def clean_contact(event):
    """Contact number box: keep digits only and stop at 11 digits."""
    box = document.querySelector("#o-contact")
    digits = "".join(ch for ch in box.value if ch.isdigit())
    box.value = digits[:11]


def show_file_name(event):
    """Show the chosen file name next to the file input."""
    name = get_selected_file()
    document.querySelector("#file-name").innerText = name or "No file selected"


def calculate_total(event):
    """Calculator (home and pricing pages). Runs on click or when an input changes."""
    size = document.querySelector("#paper-size").value
    print_type = document.querySelector("#print-type").value
    copies = read_copies(document.querySelector("#copies").value)
    total_box = document.querySelector("#total")
    error_box = document.querySelector("#calc-error")

    if copies is None:
        error_box.innerText = "Please enter a number of copies of 1 or more."
        total_box.innerText = "₱0.00"
        return

    error_box.innerText = ""
    total = PRICES[print_type][size] * copies
    total_box.innerText = f"₱{total:,.2f}"


def update_estimate(event):
    """Order form: show a live estimate when size, type, or copies change."""
    size = document.querySelector("#o-size").value
    print_type = document.querySelector("#o-type").value
    copies = read_copies(document.querySelector("#o-copies").value)

    if size and print_type and copies:
        total = PRICES[print_type][size] * copies
        document.querySelector("#o-estimate").innerText = f"₱{total:,.2f}"
    else:
        document.querySelector("#o-estimate").innerText = "₱0.00"


def submit_order(event):
    """Order form: validate the fields, then show the confirmation."""
    event.preventDefault()          # stop the page from refreshing

    name = document.querySelector("#o-name").value.strip()
    contact = document.querySelector("#o-contact").value.strip()
    size = document.querySelector("#o-size").value
    print_type = document.querySelector("#o-type").value
    copies = read_copies(document.querySelector("#o-copies").value)
    file_name = get_selected_file()

    # Collect friendly error messages
    errors = []
    if name == "":
        errors.append("Please enter your full name.")
    if contact == "":
        errors.append("Please enter your contact number.")
    elif not contact.isdigit():
        errors.append("Contact number must contain numbers only.")
    elif len(contact) != 11:
        errors.append("Contact number must contain exactly 11 digits.")
    if file_name is None:
        errors.append("Please select the file you want to print.")
    elif not file_name.lower().endswith(FILE_TYPES):
        errors.append("Please choose a PDF, DOC, DOCX, JPG, JPEG, or PNG file.")
    if size == "":
        errors.append("Please select a paper size.")
    if print_type == "":
        errors.append("Please select a printing type.")
    if copies is None:
        errors.append("Please enter a number of copies of 1 or more.")

    error_box = document.querySelector("#order-error")
    result_box = document.querySelector("#order-result")

    if errors:
        error_box.innerHTML = "<br>".join(errors)
        result_box.hidden = True
        return

    # Everything is valid: calculate and show the confirmation
    error_box.innerText = ""
    total = PRICES[print_type][size] * copies
    document.querySelector("#r-name").innerText = name
    document.querySelector("#r-contact").innerText = contact
    document.querySelector("#r-file").innerText = file_name
    document.querySelector("#r-type").innerText = TYPE_NAMES[print_type]
    document.querySelector("#r-size").innerText = SIZE_NAMES[size]
    document.querySelector("#r-copies").innerText = str(copies)
    document.querySelector("#r-total").innerText = f"₱{total:,.2f}"
    result_box.hidden = False


def clear_form(event):
    """Order form: reset every field and remove messages."""
    document.querySelector("#order-form").reset()
    document.querySelector("#order-error").innerText = ""
    document.querySelector("#order-result").hidden = True
    document.querySelector("#o-estimate").innerText = "₱0.00"
    document.querySelector("#file-name").innerText = "No file selected"