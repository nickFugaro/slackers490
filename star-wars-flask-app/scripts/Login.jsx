import React, {useState, useEffect} from 'react'
import Paper from '@material-ui/core/Paper';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Chip from '@material-ui/core/Chip';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import GoogleLogin from 'react-google-login';
import * as SocketIO from 'socket.io-client';

export var socket = SocketIO.connect();

const useStyles = makeStyles((theme) => ({
    root: {
    margin: '50px',
    padding: theme.spacing(3,2),
    backgroundColor: 'black'
    },
    
    flex: {
        display: 'flex',
        alignItems: 'center'
    },
    
    topics: {
        width: '30%',
        height: '300px',
        borderRight: '1px solid grey',
        
    },
    
    chat: {
        width: '70%',
        height: '300px',
        padding: '20px',
        overflowY: 'auto'
    },
    
    chatbox: {
        width: '85%',
        color: "white",
        backgroundColor: "white"
        
    },
    
    button: {
        width: '15%',
        top: '10px'
       
    },
    spacer: {
        width: '5px',
       
    },
    topic:{
        color: "blue",
    },
    text:{
        color: "white"
    }
}));

export default function Login(props){
    
    
    const classes = useStyles();   
    
 
    const [userName, setUserName] = useState("");
   
   
    const onChange = (event) => {
      setUserName(event.target.value);
    };

    const onClick = () => {
      setUserName("");
      props.setUsername(userName);
      props.setLoggedIn(true);
    };
    
    function handleGoogleLogin(event) {
         console.log(event.getBasicProfile().getName());
         console.log(event.getBasicProfile().getImageUrl());
         console.log(event.getBasicProfile().getEmail());
         console.log(event.getAuthResponse().id_token);
         //socket.emit('google_login', {'idtoken': event.getAuthResponse().id_token, 'name' : event.getBasicProfile().getName(), 'email' : event.getBasicProfile().getEmail(), 'image' : event.getBasicProfile.getImageUrl()});
         props.setUsername(event.getBasicProfile().getName());
         props.setImage(event.getBasicProfile().getImageUrl());
         props.setEmail(event.getBasicProfile().getEmail());
         props.setToken(event.getAuthResponse().id_token);
         props.setGoogleLogin(true);
         props.setLoggedIn(true);
        
    }
      
    const responseGoogle = (response) => {
        console.log(response);
    }

    function message_enter(e){
        if(e.key === "Enter"){
            onClick(e);
        }
    }
    
    return (
        <div>
            <Paper className={classes.root} elevation={3}>
               <center><Typography className={classes.text} variant="h4" component="h3">
               Login
               </Typography>
                </center>
               <div>
                    <div>
                         <TextField label="Username" variant="outlined" className={classes.chatbox} value={userName} onChange={onChange} color="secondary" onKeyDown={message_enter} />
                         <Button variant="contained" style={{backgroundColor: 'red'}} onClick={onClick} value="Send" className={classes.button}>
                            Login
                         </Button>
                         <center>
                         <br />
                         <GoogleLogin
                                clientId="161766459403-fh1ligbs7qp49qq9tl16ndrtl9ia712a.apps.googleusercontent.com"
                                buttonText="Login"
                                onSuccess={handleGoogleLogin}
                                onFailure={responseGoogle}
                                cookiePolicy={'single_host_origin'}
                         /></center>
                    </div>
               </div>
            
            </Paper>
        </div>
    )
}