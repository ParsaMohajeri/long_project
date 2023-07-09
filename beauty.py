import tkinter as tk
import sys
import analog_clock as ac
sys.path.insert(1,"C:/Users/bcz/Desktop/first long project/src/databases")
import db_connection as db
import json

with open('./asset/info.json', 'r') as f:
    password = json.load(f)['password']

root = tk.Tk()
root.title("Login")


def app():
    # define the function to check the password and proceed to main app
    # ac.analog_clock()
    def check_password():
        if password_entry.get() == password:
            root.destroy()
            main_app()
        else:
            password_entry.delete(0, tk.END)
            password_entry.insert(0, "Incorrect Password")
        

    # create the password entry field and login button
    password_label = tk.Label(root, text="Password:")
    password_entry = tk.Entry(root, show="*")
    login_button = tk.Button(root, text="Login", command=check_password)

    # layout the widgets in the window
    password_label.grid(row=0, column=0)
    password_entry.grid(row=0, column=1)
    login_button.grid(row=1, column=0, columnspan=2)

    # create a tkinter window for the messaging app
    def main_app():
        window = tk.Tk()
        window.title("Messaging App")


        # function to send a message to the database
        def send_message():
            message_text = message_entry.get().strip()
            if not message_text:
                message_entry.delete(0, tk.END)
                return

            try:
                sql = "INSERT INTO messenger (SMS) VALUES (%s)"
                val=(message_text,)
                db.Activator.execute(sql, val)
                db.connecting.commit()
                message_box.insert(tk.END, "\n" + message_text)
                message_entry.delete(0, tk.END)
            except:
                message_box.insert(tk.END, "\nError sending message")

        # function to update the selected message in the database
        def update_message():
            try:
                selected_message = message_box.get(tk.ACTIVE)
                new_message_text = message_entry.get()

                # return if nothing changed
                if new_message_text == selected_message:
                    return

                sql = "UPDATE messenger SET SMS = %s WHERE SMS = %s"
                val = (new_message_text, selected_message,)
                db.Activator.execute(sql, val)
                db.connecting.commit()

                # replace the original entry with the new text
                message_box.delete(tk.ACTIVE)
                message_box.insert(tk.ACTIVE, new_message_text)
                message_entry.delete(0, tk.END)
            except Exception as e:
                message_entry.insert(0, f"Error updating message: {e}")

        # function to delete the selected message from the database
        def delete_message():
            try:
                selected_message = message_box.get(tk.ACTIVE)

                sql = "DELETE FROM messenger WHERE SMS = %s"
                val = (selected_message,)
                db.Activator.execute(sql, val)
                db.connecting.commit()

                # remove the selected entry from the listbox
                message_box.delete(tk.ACTIVE)
            except Exception as e:
                message_box.insert(tk.END, f"\nError deleting message: {e}")

        # create the message box and scrollbar
        message_label = tk.Label(window, text="Messages:")
        message_scrollbar = tk.Scrollbar(window)
        message_box = tk.Listbox(window, yscrollcommand=message_scrollbar.set)
        message_scrollbar.config(command=message_box.yview)
        message_label.pack(side=tk.TOP)
        message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # create the message entry field and send button
        message_entry = tk.Entry(window)
        send_button = tk.Button(window, text="Send", command=send_message)
        message_entry.pack(side=tk.TOP, fill=tk.X, expand=True)
        send_button.pack(side=tk.TOP)

        # create the update, delete, and new message widgets
        button_frame = tk.Frame(window)
        update_button = tk.Button(button_frame, text="Update", command=update_message)
        delete_button = tk.Button(button_frame, text="Delete", command=delete_message)
        # new_message_entry_label = tk.Label(button_frame, text="New Message:")
        # new_message_entry = tk.Entry(button_frame)
        update_button.pack(side=tk.LEFT)
        delete_button.pack(side=tk.LEFT)
        # new_message_entry_label.pack(side=tk.LEFT)
        # new_message_entry.pack(side=tk.LEFT)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # populate the message box with existing messages from the database
        try:
            db.Activator.execute("SELECT SMS FROM messenger")
            messages = db.Activator.fetchall()
            for message in messages:
                message_box.insert(tk.END, message[0])
        except:
            message_box.insert(tk.END, "Error retrieving messages from database")

        # layout the widgets in the window

        window.mainloop()
    root.mainloop()

