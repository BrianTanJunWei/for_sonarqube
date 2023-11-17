import React from 'react';

function ForgetPasswordForm({ email, setEmail, handleResetPassword, message }) {
  const customMarginLeft = '20px'; // Add your desired left margin here

  return (
    <div
      className="container my-5 d-flex justify-content-center align-items-center"
      style={{ marginLeft: customMarginLeft }}
    >
      <div className="card">
        <div className="card-body">
          <h2 className="card-title">Forgot Password</h2>
          <p className="card-text">Enter your email address to reset your password.</p>

          <form>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                className="form-control"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <button
              type="button"
              className="btn btn-primary btn-block"
              onClick={handleResetPassword}
            >
              Reset Password
            </button>
          </form>

          {message && (
        <p className="mt-3 alert alert-info">
          If you have an email with us, the reset link will be sent to your email address. Thank you.
        </p>
      )}
        </div>
      </div>
    </div>
  );
}

export default ForgetPasswordForm;
