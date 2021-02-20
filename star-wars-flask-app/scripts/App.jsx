import React, {useState} from 'react';
import Dashboard from './Dashboard';
import Login from './Login';

export default function App(){
    const [loggedIn, setLoggedIn] = useState(false);
    const [googleLogin, setGoogleLogin] = useState(false);
    const [username, setUsername] = useState("");
    const [image, setImage] = useState("");
    const [email, setEmail] = useState("");
    const [token, setToken] = useState("");
    
    return loggedIn ? <Dashboard username={username} image={image} email={email} token={token} googleLogin={googleLogin} /> : <Login setUsername={setUsername} setImage={setImage} setEmail={setEmail} setToken={setToken} setGoogleLogin={setGoogleLogin} setLoggedIn={setLoggedIn}/>
    
}