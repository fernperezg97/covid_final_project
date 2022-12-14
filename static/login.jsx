// Login page where user can enter first name, last name, email, and password

// import React, { useState } from "react";

function Login() {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const submitUserLoginInfo = (e) => {
        // e.preventDefault();
        console.log("submitUserLogin function was called.");

        fetch(`/user-login-info`,{
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
            },
            body:JSON.stringify({'email': email, 'password': password})
            })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                if (responseData.result === 'unsuccessful') {
                    alert(responseData.status);
                    // console.log("alert");
                    ReactDOM.render(<Login/>, document.querySelector('#root'));
                } else {
                    // console.log("login successful");
                    window.location.href = '/covid-timeline'
                }
        });
    }

    return (
        <div className="box-form">
            <div className="left">
                <div className="overlay">
                    <h1>COVID-19</h1>
                    <h2>Choro-Tracker</h2>
                    <p>Learn about the growth and decline of COVID-19 cases and deaths around the world through an interactive choropleth map.</p>
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
               
                <br />
                {/* <button onClick={() => props.onFormSwitch('register')}>Login</button> */}
                <button type="submit" onClick={submitUserLoginInfo}>Login</button>
            </div>
        </div>
    );
}

ReactDOM.render(<Login/>, document.querySelector('#root'));