menu = {
    1: {"food": "Rice and beef", "price": 6000},
    2: {"food": "Chips and chicken", "price": 8000},
    3: {"food": "Rolex", "price": 2500},
    4: {"food": "Fried Chicken", "price": 7000},
    5: {"food": "Soda", "price": 1500},
    6: {"food": "Water", "price": 1000},
    7: {"food": "Orange juice", "price": 2000},
    8: {"food": "Cocktail", "price": 2500}
}

admin_pin = "1234"
file_name = "orders.txt"
separator = "------------------------------"


# READ ALL ORDERS
def read_orders():
    try:
        with open(file_name, "r") as file:
            content = file.read()

        orders = []

        for block in content.split(separator):
            lines = block.strip().split("\n")

            if lines and lines[0].startswith("ORDER NUMBER:"):
                orders.append(lines)

        return orders

    except FileNotFoundError:
        return []


# SAVE ALL ORDERS
def save_orders(orders):
    with open(file_name, "w") as file:
        for order in orders:
            for line in order:
                file.write(line + "\n")

            file.write(separator + "\n")


# GET INFORMATION FROM AN ORDER
def get_value(order, label):
    for line in order:
        if line.startswith(label):
            return line.replace(label, "", 1).strip()

    return ""


# UPDATE INFORMATION IN AN ORDER
def update_value(order, label, new_value):
    for i in range(len(order)):
        if order[i].startswith(label):
            order[i] = label + new_value
            return


# FIND AN ORDER
def find_order(orders, order_number):
    for i in range(len(orders)):
        if get_value(orders[i], "ORDER NUMBER:") == order_number:
            return i

    return -1


# DISPLAY FOOD MENU
def display_menu():
    print("\n========== UCU CAMPUS CANTEEN ==========")
    print("              FOOD MENU")
    print("----------------------------------------")

    for number, item in menu.items():
        print(number, ".", item["food"], "- UGX", item["price"])

    print("----------------------------------------")


# PLACE AN ORDER
def place_order():
    orders = read_orders()

    print("\n========== PLACE AN ORDER ==========")

    name = input("Enter your name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    phone = input("Enter your phone number: ").strip()

    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number.")
        return

    display_menu()

    try:
        choices = input(
            "Enter food numbers separated by commas: "
        ).split(",")

        quantities = input(
            "Enter quantities separated by commas: "
        ).split(",")

        if len(choices) != len(quantities):
            print("The number of foods and quantities must match.")
            return

        cart = []
        total = 0

        for i in range(len(choices)):
            food_number = int(choices[i].strip())
            quantity = int(quantities[i].strip())

            if food_number not in menu:
                print("Invalid food selection.")
                return

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                return

            food = menu[food_number]["food"]
            price = menu[food_number]["price"]

            subtotal = price * quantity
            total += subtotal

            cart.append(
                food + " x " + str(quantity) +
                " = UGX " + str(subtotal)
            )

        print("\n========== ORDER SUMMARY ==========")

        for item in cart:
            print(item)

        print("TOTAL: UGX", total)

        confirm = input("Confirm this order? (yes/no): ").lower()

        if confirm != "yes":
            print("Order was not placed.")
            return

        print("\nSelect payment method:")
        print("1. MTN Mobile Money")
        print("2. Airtel Money")
        print("3. Bank Card")

        payment_methods = {
            1: "MTN Mobile Money",
            2: "Airtel Money",
            3: "Bank Card"
        }

        try:
            payment_choice = int(input("Choose payment method: "))

            if payment_choice not in payment_methods:
                print("Invalid payment method.")
                return

        except ValueError:
            print("Please enter a valid number.")
            return

        order_number = "UCU" + str(len(orders) + 1)

        new_order = [
            "ORDER NUMBER: " + order_number,
            "Customer: " + name,
            "Contact: " + phone
        ]

        new_order.extend(cart)

        new_order.extend([
            "Total: UGX " + str(total),
            "Payment Method: " + payment_methods[payment_choice],
            "Payment Status: Pending",
            "Order Status: Awaiting Payment"
        ])

        orders.append(new_order)
        save_orders(orders)

        print("\nOrder successfully placed!")
        print("Your order number is:", order_number)
        print("Payment Status: Pending")
        print("Please complete your payment.")

    except ValueError:
        print("Invalid input. Please enter numbers correctly.")


# CANCEL AN ORDER
def cancel_order():
    orders = read_orders()

    print("\n========== CANCEL AN ORDER ==========")

    order_number = input("Enter your order number: ").strip().upper()
    phone = input("Enter the phone number used for the order: ").strip()

    order_index = find_order(orders, order_number)

    if order_index == -1:
        print("Order not found.")
        return

    order = orders[order_index]

    # CHECK CUSTOMER PHONE NUMBER
    saved_phone = get_value(order, "Contact:")

    if phone != saved_phone:
        print("Phone number does not match this order.")
        return

    current_status = get_value(order, "Order Status:")

    # CHECK WHETHER CANCELLATION IS ALLOWED
    if current_status not in ["Awaiting Payment", "Confirmed"]:
        print("This order cannot be cancelled.")
        print("Current order status:", current_status)
        return

    print("\nOrder found!")
    print("Order Number:", order_number)
    print("Customer:", get_value(order, "Customer:"))
    print("Total:", get_value(order, "Total:"))
    print("Payment Status:", get_value(order, "Payment Status:"))

    print("\nIMPORTANT CANCELLATION POLICY")
    print("1. Cancelling an order does not qualify for a refund.")
    print("2. If payment was already made, it will remain recorded as Paid.")
    print("3. The order will be permanently marked as Cancelled - No Refund.")

    confirm = input(
        "\nDo you accept this policy and want to cancel? (yes/no): "
    ).lower()

    if confirm == "yes":
        update_value(
            order,
            "Order Status:",
            "Cancelled - No Refund"
        )

        save_orders(orders)

        print("\nYour order has been cancelled.")
        print("No refund will be issued.")
        print("Payment record:", get_value(order, "Payment Status:"))

    elif confirm == "no":
        print("Cancellation stopped. Your order remains active.")

    else:
        print("Invalid choice. Order was not cancelled.")


# STAFF VIEW ALL ORDERS
def view_orders():
    orders = read_orders()

    print("\n========== ALL CANTEEN ORDERS ==========")

    if not orders:
        print("No orders available.")
        return

    for order in orders:
        for line in order:
            print(line)

        print(separator)


# STAFF VERIFY PAYMENTS
def verify_payment():
    orders = read_orders()

    print("\n========== VERIFY PAYMENT ==========")

    order_number = input("Enter order number: ").strip().upper()

    index = find_order(orders, order_number)

    if index == -1:
        print("Order not found.")
        return

    order = orders[index]

    payment_status = get_value(order, "Payment Status:")
    order_status = get_value(order, "Order Status:")

    if order_status.startswith("Cancelled"):
        print("This order has been cancelled.")
        print("Payment status:", payment_status)
        return

    if payment_status != "Pending":
        print("Payment has already been marked:", payment_status)
        return

    print("\n1. Mark as Paid")
    print("2. Mark as Failed")
    print("3. Leave Pending")

    try:
        choice = int(input("Choose an option: "))

        if choice == 1:
            verified = input(
                "Have you checked the actual payment records? (yes/no): "
            ).lower()

            if verified == "yes":
                update_value(order, "Payment Status:", "Paid")
                update_value(order, "Order Status:", "Confirmed")

                save_orders(orders)

                print("Payment verified successfully.")

            elif verified == "no":
                print("Payment remains Pending.")

            else:
                print("Invalid response.")

        elif choice == 2:
            update_value(order, "Payment Status:", "Failed")
            update_value(order, "Order Status:", "Payment Failed")

            save_orders(orders)

            print("Payment marked as Failed.")

        elif choice == 3:
            print("Payment remains Pending.")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Please enter a valid number.")


# STAFF UPDATE ORDER STATUS
def update_order_status():
    orders = read_orders()

    print("\n========== UPDATE ORDER STATUS ==========")

    order_number = input("Enter order number: ").strip().upper()

    index = find_order(orders, order_number)

    if index == -1:
        print("Order not found.")
        return

    order = orders[index]

    payment_status = get_value(order, "Payment Status:")
    current_status = get_value(order, "Order Status:")

    if payment_status != "Paid":
        print("This order has not been paid for.")
        return

    if current_status.startswith("Cancelled"):
        print("This order has already been cancelled.")
        return

    if current_status == "Collected":
        print("This order has already been collected.")
        return

    print("\nSelect new order status:")
    print("1. Preparing")
    print("2. Ready for Pickup")
    print("3. Collected")
    print("4. Cancelled - No Refund")

    try:
        choice = int(input("Choose an option: "))

        statuses = {
            1: "Preparing",
            2: "Ready for Pickup",
            3: "Collected",
            4: "Cancelled - No Refund"
        }

        if choice not in statuses:
            print("Invalid choice.")
            return

        if choice == 4:
            print("\nCancellation policy: No refund will be issued.")

            confirm = input("Confirm cancellation? (yes/no): ").lower()

            if confirm != "yes":
                print("Cancellation stopped.")
                return

        update_value(order, "Order Status:", statuses[choice])

        save_orders(orders)

        print("Order status updated successfully.")

    except ValueError:
        print("Please enter a valid number.")


# STAFF DASHBOARD
def staff_login():
    print("\n========== STAFF LOGIN ==========")

    attempts = 3

    while attempts > 0:
        pin = input("Enter admin PIN: ")

        if pin == admin_pin:
            print("Login successful!")

            while True:
                print("\n========== STAFF DASHBOARD ==========")
                print("1. View All Orders")
                print("2. Verify Payments")
                print("3. Update Order Status")
                print("4. Return to Main Menu")

                try:
                    choice = int(input("Choose an option: "))

                    if choice == 1:
                        view_orders()

                    elif choice == 2:
                        verify_payment()

                    elif choice == 3:
                        update_order_status()

                    elif choice == 4:
                        break

                    else:
                        print("Invalid choice.")

                except ValueError:
                    print("Please enter a number.")

            return

        else:
            attempts -= 1
            print("Incorrect PIN. Attempts remaining:", attempts)

    print("Access denied.")


# MAIN PROGRAM
while True:

    print("\n========================================")
    print("       UCU CAMPUS CANTEEN SYSTEM")
    print("========================================")

    print("1. Place an Order")
    print("2. Cancel an Order")
    print("3. Staff Login")
    print("4. Exit")

    try:
        choice = int(input("Choose an option: "))

        if choice == 1:
            place_order()

        elif choice == 2:
            cancel_order()

        elif choice == 3:
            staff_login()

        elif choice == 4:
            print("Thank you for using UCU Campus Canteen!")
            break

        else:
            print("Invalid choice. Please try again.")
            continue

        print("\n1. Return to Main Menu")
        print("2. Exit")

        next_choice = input("Choose an option: ")

        if next_choice == "2":
            print("Thank you for using UCU Campus Canteen!")
            break

        elif next_choice != "1":
            print("Invalid choice. Returning to Main Menu.")

    except ValueError:
        print("Please enter a valid number.")