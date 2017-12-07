'use strict';

import React from 'react';
import { Typeahead } from 'react-bootstrap-typeahead';
import GAMES from '../games.js';

let optionSelected = function(result) {
    console.log(GAMES[result]);
}

class Main extends React.Component {
    state = {
        ratings: [],
        recommendations: []
    };

    render() {
        return (
            <div>
                <div className="row">
                    <h2>VGML</h2>
                </div>
                <div className="typeahead">
                        <Typeahead
                            multiple
                            onChange={selected => {
                                this.state.ratings = selected.map(obj => { return { id: obj.id, rating: 200 }});
                            }}
                            labelKey={'game'}
                            options={GAMES}
                            maxResults={10}
                        />
                        <button className="btn-secondary" onClick={() => {
                            console.log(this.state);
                            fetch("http://54.174.204.120:5432/ratings", {
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                method: "POST",
                                body: JSON.stringify(this.state)
                            }).then(response => {
                                return response.json();
                            }).then(obj => {
                                console.log(obj);
                            });
                        }}>
                            Submit
                        </button>
                </div>
            </div>
        );
    }
}

export default Main;