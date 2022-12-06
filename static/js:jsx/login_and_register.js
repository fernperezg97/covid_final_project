import '/static/login.css';
import { login } from "/static/login.jsx"
import { register } from "/static/register.jsx"


function loginAndRegister() {
    const [currentForm, setCurrentForm] = useState('login');

    const toggleForm = (formName) => {
        setCurrentForm(formName);
    }

    return (
        <div className="loginAndRegister">
            {
                currentForm === "login" ? <login onFormSwitch={toggleForm} /> : <register onFormSwitch={toggleForm} />
            }   
        </div>
    );
}

export default login;