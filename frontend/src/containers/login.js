import React, { useState } from "react";

export const Login = (props) => {
    const [userName, setUserName] = useState('');
    const [userID, setUserID] = useState('');
    const [pass, setPass] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(userName);
    }

    function validateForm() {
        return userName.length > 0 && userID.length > 0 && pass.length > 0
    }

    return (
        <div className="auth-form-container">
            <h2>Login</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input value={userName} onChange={(e) => setUserName(e.target.value)}type="username" placeholder="username" id="username" name="username" />
                <label htmlFor="user id">User ID</label>
                <input value={userID} onChange={(e) => setUserID(e.target.value)}type="user-id" placeholder="user id" id="user-id" name="user-id" />
                <label htmlFor="password">Password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                <button className="action-btn" type="login" disabled={!validateForm()}>Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('register')}>Don't have an account? Register here.</button>
        </div>
    )
}