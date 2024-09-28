import React from 'react';
import "./login.css";

const Login = () => {
    return (
        <div className="container">
            <div className="header">
                <div className="text">HackerMatch Login</div>
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="email" placeholder="Email" />
                </div>
                <div className="input">
                    <input type="password" placeholder="Password" />
                </div>
                <div className="button-container">
                    <button type="submit">Login</button>
                </div>
            </div>
        </div>
    );
}

export default Login;
