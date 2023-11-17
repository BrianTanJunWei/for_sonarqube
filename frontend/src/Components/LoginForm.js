// components/LoginForm.js
import React from 'react';

const LoginForm = ({
    email,
    password,
    handleEmailChange,
    handlePasswordChange,
    handleLogin,
    role, // Add the role prop
}) => (
    <div className="login-form">
        <h2>Login</h2>
        <form>
            <div>
                <label>Email:</label>
                <input
                    type="email"
                    value={email}
                    onChange={handleEmailChange}
                    required
                />
            </div>
            <div>
                <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={handlePasswordChange}
                    required
                />
            </div>
            <div className="login-buttons">
                {role === "admin" ? (
                    // Admin Login
                    <button
                        type="button"
                        className="custom-button"
                        onClick={handleLogin}
                    >
                        Login
                    </button>
                ) : (
                    // Buyer or Seller Login
                    <>
                        <button
                            type="button"
                            className="custom-button"
                            onClick={(e) => handleLogin('Buyer', e)}
                        >
                            Login as Buyer
                        </button>
                        <button
                            type="button"
                            className="custom-button"
                            onClick={(e) => handleLogin('Seller', e)}
                        >
                            Login as Seller
                        </button>
                    </>
                )}
            </div>
        </form>
    </div>
);

export default LoginForm;
