package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"gopkg.in/gomail.v2"
)

type EmailRequest struct {
	ChildEmail string `json:"child_email"`
	Amount     float64 `json:"amount"`
	ClassName  string `json:"class_name"`
}

func sendEmailHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	var emailReq EmailRequest
	if err := json.NewDecoder(r.Body).Decode(&emailReq); err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	// Set up email message
	d := gomail.NewDialer("smtp.example.com", 587, "your_email@example.com", "your_password")
	m := gomail.NewMessage()
	m.SetHeader("From", "your_email@example.com")
	m.SetHeader("To", emailReq.ChildEmail)
	m.SetHeader("Subject", fmt.Sprintf("Payment Received for %s", emailReq.ClassName))
	m.SetBody("text/plain", fmt.Sprintf("Dear student,\n\nA payment of %.2f has been successfully recorded for your class %s.\n\nBest regards,\nYour School", emailReq.Amount, emailReq.ClassName))

	// Send email
	if err := d.DialAndSend(m); err != nil {
		log.Printf("Error sending email: %v", err)
		http.Error(w, "Failed to send email", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Email sent successfully"))
}

func main() {
	http.HandleFunc("/send-email", sendEmailHandler)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Starting server on :%s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}
