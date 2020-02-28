import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import Timer from "react-compound-timer"

import axios from 'axios';

function App(props) {

    const [todo, setTodo] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/').then(res => {
            setTodo(res.data);
        }) .catch(err => {
            console.log(err);
        });
    }, [todo]);

    const buttonClickHandler = () => {
        setTodo(todo.concat([`${document.getElementById("name").value}, time: ${document.getElementById("time").children[0].innerText}`]))
        document.getElementById("name").value = "";
    };

    const deleteEntryHandler = (event) => {
        console.log("clicked");
        let id = +event.target.id;
        setTodo(todo.slice(0, id).concat(todo.slice(id + 1)));
    };

    return (
        <div className="App" style = {{width: "100%"}}>
            <header
                style = {{display: "flex", flexDirection: "column", justifyContent: "center"}}
            >
                <input type = "text" id = "name" placeholder = "Введите название заметки" style = {{
                    marginTop:   "20px",
                    marginLeft: "300px",
                    marginRight: "300px"
                }}/>
                <input type = "button" value="add" style = {{
                    marginTop: "20px",
                    marginLeft: "500px",
                    marginRight: "500px"
                }} onClick = {buttonClickHandler}/>
                <p id = "time">
                    <Timer>
                        {({ start, resume, pause, stop, reset, timerState }) => (
                            <React.Fragment>
                                <div>
                                    <Timer.Hours formatValue={value => `${(value < 10 ? `0${value}` : value)}:`} />
                                    <Timer.Minutes formatValue={value => `${(value < 10 ? `0${value}` : value)}:`} />
                                    <Timer.Seconds formatValue={value => `${(value < 10 ? `0${value}` : value)}`} />
                                </div>
                                <div>{timerState}</div>
                                <div>
                                    <button onClick={start}>Start</button>
                                    <button onClick={pause}>Pause</button>
                                    <button onClick={resume}>Resume</button>
                                    <button onClick={stop}>Stop</button>
                                    <button onClick={reset}>Reset</button>
                                </div>
                            </React.Fragment>
                        )}
                    </Timer>
                </p>
            </header>
            <main style = {{border: "1px solid black", minHeight: "400px", marginLeft: "300px", marginRight: "300px"}}>
                <p>Тут заметки</p>
                {todo.map((t, i) => (<p id = {i} onClick = {deleteEntryHandler}>{t}</p>))}
            </main>
        </div>
    );
}

export default App;
