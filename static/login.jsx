// Login page where user can enter first name, last name, email, and password

// import React, { useState } from "react";

function Login() {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const submitUserLoginInfo = (e) => {
        e.preventDefault();
        // console.log(email);

        fetch(`/user-login-info`,{
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
            },
            body:JSON.stringify({'email': email, 'password': password})
        })
    }

    return (
        <div className="box-form">
            <div className="left">
                <div className="overlay">
                    <h1>Hello World.</h1>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                        Curabitur et est sed felis aliquet sollicitudin</p>
                </div>
            </div>
            <div className="right">
                <h5>Login</h5>
                <p>Don't have an account? <a href="/register">Create Your Account</a> it takes less than a minute.</p>
                <div className="inputs">
                    <input value={email} onChange={(e) => setEmail(e.target.value)} type="text" placeholder="email" />
                    <br />
                    <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="password" />
                </div>
                <br /><br />
                <div className="remember-me--forget-password">
                    {/* Angular */}
                <label>
                    <input type="checkbox" name="item" defaultChecked />
                    <span className="text-checkbox">Remember me</span>
                </label>
                <p>forget password?</p>
                </div>
                <br />
                {/* <button onClick={() => props.onFormSwitch('register')}>Login</button> */}
                <button type="submit" onClick={submitUserLoginInfo}>Login</button>
            </div>
        </div>
    );
}

ReactDOM.render(<Login/>, document.querySelector('#root'));