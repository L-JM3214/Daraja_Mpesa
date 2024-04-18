import React, { useState } from "react";
import { Link } from "react-router-dom";
import safcomLogo from "../assets/safcom.png";
import mpesaLogo from "../assets/mpesa.png";

const MpesaPaymentPage = () => {
  const initialFormData = {
    phone: "",
    amount: "",
  };

  const [formData, setFormData] = useState(initialFormData);
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const submitForm = (event) => {
    event.preventDefault();
    setLoading(true);

    fetch("http://127.0.0.1:5000/payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        setLoading(false);

        if (response.ok) {
          window.alert("Payment made");
          setFormData(initialFormData);
        } else {
          window.alert("Payment processing");
        }
      })
      .catch((error) => {
        setLoading(false);
        console.error("Error: ", error);
      });
  };

  return (
    <div>
      <div className="login-dialogue">
        <div className="form-dialogue">
          <div className="logo-container">
            <img src={safcomLogo} alt="Safcom Logo" />
            <img src={mpesaLogo} alt="Mpesa Logo" />
          </div>
          <form onSubmit={submitForm}>
            <h2>Pay Here &#128512;</h2>
            <h5>Add your phone number and amount :</h5>
            <div className="form-itemP">
              <label htmlFor="phone">Phone:</label>
              <input
                type="number"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-item">
              <label htmlFor="amount">Amount:</label>
              <input
                type="number"
                id="amount"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-buttons">
              <button
                type="submit"
                className="continue-shopping"
                disabled={loading}
              >
                {loading ? "Processing..." : "Submit"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default MpesaPaymentPage;


