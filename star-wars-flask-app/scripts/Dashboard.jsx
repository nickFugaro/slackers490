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
import * as SocketIO from 'socket.io-client';
import ScrollToBottom from 'react-scroll-to-bottom';

export var socket = SocketIO.connect();


const useStyles = makeStyles((theme) => ({
    root: {
        margin: '50px',
        padding: theme.spacing(3,2),
        backgroundColor: 'black',
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
    },
    
    pic:{
        position: 'relative', 
	    top: '10px',
	    right : '5px'
    },
    
    chip:{
        position: 'relative', 
	    right: '2px',
    }
}));

export default function Dashboard(props){
    
    
    const classes = useStyles();   
    
    const [userCount, setUserCount] = useState(0);
    const [users, setUser] = useState([]);
    const [messages, setMessages] = useState([]);
    const [images, setImages] = useState([]);
    const [message, setMessage] = useState("");
   
   //Usestate is gonna be a list of JSON objects
   
   useEffect(() => {
    socket.emit('messages requested')}, []);
   
   useEffect(() => {
    socket.emit('usercount requested')}, []);
   //TODO check what is printing
   
   useEffect(()=> {
    socket.on("messages received", (msg) => {
    setMessages(msg['allMessages'])})},[]);
   
   useEffect(()=> {
    socket.on("messages received", (usr) => {
    setUser(usr['allUsers'])})},[]);
    
   useEffect(()=> {
    socket.on("messages received", (img) => {
    setImages(img['allImages'])})},[]);
   
   useEffect(()=> {
    socket.on("message&user", (msg) => {
    setMessages(prevMessages => [...prevMessages, msg['message']])})},[]);
    
   useEffect(()=> {
    socket.on("message&user", (usr) => {
    setUser(prevUsers => [...prevUsers, usr['user']])})},[]);
    
   useEffect(()=> {
    socket.on("message&user", (img) => {
    setImages(prevImages => [...prevImages, img['image']])})},[]);
   
   useEffect(()=> {
    socket.on("userNum", (data) => {
    setUserCount(data['count'])})},[]);
    
   useEffect(()=> {
    socket.on("newUser", (data) => {
    setUserCount(data['count'])})},[]);
   
   useEffect(()=> {
    socket.on("lessUser", (data) => {
    setUserCount(data['count'])})},[]);

    const onChange = (event) => {
      setMessage(event.target.value);
    };

    const onClick = () => {
        if(props.googleLogin){
            console.log("Google Good");
            console.log(message);
            console.log(props.username);
            socket.emit("google_login", {'message' : message, 'user' : props.username, 'tokenid' : props.token , 'email' : props.email, 'image' : props.image});
            setMessage("");
        }
        else{
            socket.emit("message_user", {'message': message, 'user': props.username});
            setMessage("");
        }
    };

    function message_enter(e){
        if(e.key === "Enter"){
            onClick(e);
        }
    }
    
    return (
        <div>
            <Paper className={classes.root} elevation={3}>
               <center><Typography className={classes.text} variant="h4" component="h3">
               Star Wars Chat App
               </Typography>
               <Typography className={classes.text} variant="h5" component="p">
               General
               </Typography>
               <Typography className={classes.text} variant="h5" component="p">
               User Count: {userCount/2}
               </Typography>
               </center>
               <div className={classes.flex}>
                    <div className={classes.topics}>
                        <List>
                                   <ListItem button>
                                    <ListItemText className={classes.text}>General</ListItemText>
                                   </ListItem> 
                        </List>
                    </div>
                    <ScrollToBottom className={classes.chat}>
                    
                                   <div className={classes.flex}>
                                    <p className={classes.spacer}/>
                                    <Typography className={classes.text} variant='body1' gutterBottom><div> 
                                   {messages.map((msg,index) =>
                                    (<div>
                                    <img style={{ height: '30px', width: '30px'}} src={images[index]} alt="Profile Pic" className={classes.pic}/>
                                    <Chip label={users[index]} className={classes.chip} style={{ backgroundColor: 'red', display: 'inline-block' }}/>
                                    <div style={{display: 'inline-block'}}dangerouslySetInnerHTML={{ __html: msg}}></div>
                                    </div>))} 
                                    </div></Typography>
                                   </div>
                                  
                    </ScrollToBottom>
               </div>
               
               <div>
                    <div>
                        
                         <TextField label="Send a Message" variant="outlined" className={classes.chatbox} value={message} onChange={onChange} color="secondary" onKeyDown={message_enter} />
                        
                         <Button variant="contained" style={{backgroundColor: 'red'}} onClick={onClick} value="Send" className={classes.button}>
                            SEND
                         </Button>
                    </div>
               </div>
            
            </Paper>
        </div>
    )
}