import { Login } from "../containers/login.js";
import { Register } from "../containers/register.js";
import React, {useEffect, useState} from "react";
import logo from '../assets/logo_white.png';


const Entry = () => {
    const [currentForm, setCurrentForm] = useState('login');
    const toggleForm = (formName) => {
        setCurrentForm(formName)
    }

    useEffect(() => {
    document.title = currentForm === 'login' ? 'Team Sprinters | Login' : 'Team Sprinters | Register';
    }, [currentForm]);


    return(
        <div className="entry">
            {/* <header className="App-header">
                <h1>Login Here!</h1>
            </header> */}
            <img src={logo} className="entry-logo" alt="logo" />
            {
                currentForm === "login" ? <Login onFormSwitch={toggleForm} /> : <Register onFormSwitch={toggleForm} />
            }
        </div>
    )
}

export default Entry;