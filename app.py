#!/usr/bin/env python
# coding: utf-8

# In[6]:


from flask import Flask, request, jsonify, render_template
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Function to send an email (Booking confirmation)
def send_email(phone, date, time, receiver_email):
    try:
        # Set up the SMTP server
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login("hotelmanagementbot@gmail.com", "irzl knhn zcby tyxl")  # Replace with valid Gmail credentials

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = "hotelmanagementbot@gmail.com"  # Sender's email address
        msg['To'] = receiver_email  # Receiver's email address from the frontend
        msg['Subject'] = "Booking Request Confirmation"

        message = f"""
        Hello team,

        This is your AI Chatbot. We received a room booking request for {date} at {time}.
        The phone number provided is {phone}.

        Thanks and Regards,
        Your AI Chatbot.
        """
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        s.send_message(msg)
        s.quit()  # Close the SMTP session
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()  # Get the message from the frontend
    receiver_email = request.json.get('receiver_email', '')  # Get the receiver's email from the frontend
    phone = request.json.get('phone', '')  # Get phone number from the frontend
    date = request.json.get('date', '')  # Get booking date from the frontend
    time = request.json.get('time', '')  # Get booking time from the frontend

    # Load intents from the JSON file
    with open('skill-Room-Booking.json', 'r') as f:
        intents = json.load(f)['intents']

    for intent in intents:
        if any(example['text'].lower() in user_message for example in intent['examples']):
            if intent['intent'] == 'Room_Bookings':
                # Trigger the email function with the receiver's email
                send_email(phone, date, time, receiver_email)
                return jsonify({"reply": f"Your room booking request for {date} at {time} has been sent to {receiver_email}!"})
            return jsonify({"reply": intent['description']})

    return jsonify({"reply": "Sorry, I didn't understand that."})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
