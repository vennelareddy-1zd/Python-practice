import streamlit as st
from datetime import datetime

# ---------------------------
# ATM Logic functions
# ---------------------------
def check_balance():
    return st.session_state.balance

def deposit(amount: float):
    if amount is None:
        return False, "Please enter an amount."
    try:
        amount = float(amount)
    except Exception:
        return False, "Invalid amount."
    if amount <= 0:
        return False, "Invalid amount. Please enter a positive value."
    if amount > 50000:
        return False, "Deposit limit exceeded. Try again (Max ₹50,000 per transaction)."
    st.session_state.balance += amount
    st.session_state.transactions.append({
        "type": "Deposit",
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True, f"Successfully deposited ₹{amount:.2f}. New balance: ₹{st.session_state.balance:.2f}"

def withdraw(amount: float):
    if amount is None:
        return False, "Please enter an amount."
    try:
        amount = float(amount)
    except Exception:
        return False, "Invalid amount."
    if amount <= 0:
        return False, "Invalid amount. Please enter a positive value."
    if amount % 100 != 0:
        return False, "Amount must be in multiples of ₹100."
    if amount > 20000:
        return False, "Withdraw limit exceeded (Max ₹20,000 per transaction)."
    if amount > st.session_state.balance:
        return False, "Insufficient funds."
    if (st.session_state.balance - amount) < 1000:
        return False, "Transaction rejected. Minimum balance of ₹1000 must be maintained."
    st.session_state.balance -= amount
    st.session_state.transactions.append({
        "type": "Withdrawal",
        "amount": amount,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True, f"Successfully withdrew ₹{amount:.2f}. New balance: ₹{st.session_state.balance:.2f}"


# ---------------------------
# Main ATM Flow (Streamlit UI)
# ---------------------------
def atm():
    st.set_page_config(page_title="ATM Simulator", layout="centered")
    st.title("🏦 ATM Machine Simulator")

    # Initialize session state
    if "pin_verified" not in st.session_state:
        st.session_state.pin_verified = False
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "balance" not in st.session_state:
        st.session_state.balance = 10000.00
    if "card_blocked" not in st.session_state:
        st.session_state.card_blocked = False
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    if "correct_pin" not in st.session_state:
        st.session_state.correct_pin = "1234"
    if "pin_input" not in st.session_state:
        st.session_state.pin_input = ""
    if "pin_message" not in st.session_state:
        st.session_state.pin_message = ""
    if "pin_status" not in st.session_state:
        st.session_state.pin_status = "info"

    # If card blocked, show message and stop
    if st.session_state.card_blocked:
        st.error("Card Blocked. Please contact bank.")
        return

    # -------------------------------
    # PIN Verification Block
    # -------------------------------
    if not st.session_state.pin_verified:
        st.subheader("Enter your 4-digit PIN")

        def submit_pin():
            pin = st.session_state.pin_input
            if not pin or len(pin.strip()) != 4 or not pin.isdigit():
                st.session_state.pin_message = "Please enter a valid 4-digit PIN."
                st.session_state.pin_status = "warning"
            else:
                st.session_state.attempts += 1
                if pin == st.session_state.correct_pin:
                    st.session_state.pin_verified = True
                    st.session_state.pin_message = "PIN verified successfully!"
                    st.session_state.pin_status = "success"
                    st.session_state.pin_input = ""
                else:
                    remaining = 3 - st.session_state.attempts
                    if remaining <= 0:
                        st.session_state.card_blocked = True
                        st.session_state.pin_message = "Card Blocked. Please contact bank."
                        st.session_state.pin_status = "error"
                    else:
                        st.session_state.pin_message = f"Incorrect PIN. {remaining} attempt(s) remaining."
                        st.session_state.pin_status = "warning"

        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("PIN", type="password", max_chars=4, key="pin_input")
        with col2:
            st.button("Submit PIN", on_click=submit_pin)

        if st.session_state.pin_message:
            status = st.session_state.pin_status
            if status == "success":
                st.success(st.session_state.pin_message)
            elif status == "warning":
                st.warning(st.session_state.pin_message)
            elif status == "error":
                st.error(st.session_state.pin_message)
            else:
                st.info(st.session_state.pin_message)

        return  # Stop here until PIN is verified

    # -------------------------------
    # Main Menu After PIN Verified
    # -------------------------------
    st.subheader("Main Menu")
    menu = st.radio("Choose an option:", ("Check Balance", "Deposit Money", "Withdraw Money", "Transaction History", "Exit"))

    if menu == "Check Balance":
        bal = check_balance()
        st.info(f"Your current balance is ₹{bal:.2f}")

    elif menu == "Deposit Money":
        st.write("Deposit Rules:")
        st.write("- Maximum ₹50,000 per transaction.")
        st.write("- Enter a positive amount.")
        amount = st.number_input("Enter amount to deposit (₹):", min_value=0.0, step=100.0, format="%f", key="deposit_amt")
        if st.button("Deposit"):
            ok, msg = deposit(amount)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    elif menu == "Withdraw Money":
        st.write("Withdrawal Rules:")
        st.write("- Amount must be in multiples of ₹100.")
        st.write("- Maximum ₹20,000 per transaction.")
        st.write("- Must maintain minimum balance of ₹1,000 after withdrawal.")
        amount = st.number_input("Enter amount to withdraw (₹):", min_value=0.0, step=100.0, format="%f", key="withdraw_amt")
        if st.button("Withdraw"):
            ok, msg = withdraw(amount)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    elif menu == "Transaction History":
        st.write("Recent Transactions:")
        txs = st.session_state.transactions[::-1]
        if not txs:
            st.info("No transactions yet.")
        else:
            for t in txs:
                st.write(f"- **{t['type']}** ₹{t['amount']:.2f}  — {t['time']}")

    elif menu == "Exit":
        st.success("Thank you for banking with us!")
        st.session_state.pin_verified = False

    st.markdown("---")
    st.caption("Demo ATM built with Streamlit. For production, do not store PINs in plain variables.")


# ---------------------------
# Entrypoint
# ---------------------------
if __name__ == "__main__":
    atm()
