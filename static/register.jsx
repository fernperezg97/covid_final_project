// Allows the user the option to register if they are new.

function Register(props) {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
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
                <h5>Register</h5>
                <p>Already have an account? <a href="/login">Login here</a> and navigate to your existing account.</p>
                <div className="inputs">
                    <input type="text" placeholder="first name" />
                    <br />
                    <input type="password" placeholder="last name" />
                    <br />
                    <input type="text" placeholder="email" />
                    <br />
                    <input type="password" placeholder="password" />
                </div>
                <br /><br />
                <div className="remember-me--forget-password">
                {/* Angular */}
                {/* <label>
                    <input type="checkbox" name="item" defaultChecked />
                    <span className="text-checkbox">Remember me</span>
                </label> */}
                {/* <p>forget password?</p> */}
                </div>
                <br />
                <button onClick={() => props.onFormSwitch('login')}>Register</button>
            </div>
        </div>
    );
}

ReactDOM.render(<Register/>, document.querySelector('#root'));