// Allows the user the option to register if they are new.

function Register() {
    const [firstName, setFirstName] = React.useState('');
    const [lastName, setLastName] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const submitUserRegisterInfo = (e) => {
        // e.preventDefault();
        // console.log(firstName, lastName, email, password);

        fetch(`/user-registration-check`, {
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
            },
            body:JSON.stringify({'firstName': firstName, 'lastName': lastName, 'email': email, 'password': password})
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                if (responseData.result === 'unsuccessful') {
                    swal({
                        title: "Invalid Credentials!",
                        text: "User already exists or input is invalid.",
                        icon: "error",
                        button: true,
                        dangerMode: true,
                      });
                } else {
                    swal({title: "New User Created!",
                        text: "You will be redirected to login with your new credentials.",
                        icon: "success",
                        button: "OK"})
                    .then(() => {
                        window.location.href = '/login';
                });
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
                <h5>Register</h5>
                <p>Already have an account? <a href="/login">Login here</a> and navigate to your existing account.</p>
                <div className="inputs">
                    <input value={firstName} onChange={(e) => setFirstName(e.target.value)} type="text" placeholder="first name" />
                    <br />
                    <input value={lastName} onChange={(e) => setLastName(e.target.value)} type="text" placeholder="last name" />
                    <br />
                    <input value={email} onChange={(e) => setEmail(e.target.value)} type="text" placeholder="email" />
                    <br />
                    <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="password" />
                </div>
                <br /><br />
                <button type="button" onClick={submitUserRegisterInfo}>Register</button>
            </div>
        </div>
    );
}

ReactDOM.render(<Register/>, document.querySelector('#root'));