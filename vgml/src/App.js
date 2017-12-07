import React, { Component } from 'react';
import { BrowserRouter, Route, Redirect } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import './bootstrap.css';

import Main from './components/main';

class App extends Component {
  render() {
    return <BrowserRouter>
      <Route exact path="/" component={Main}/>
    </BrowserRouter>
  }
}

export default App;
