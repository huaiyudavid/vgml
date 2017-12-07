'use strict';

import React from 'react';
import { Typeahead } from 'react-bootstrap-typeahead';
import GAMES from '../games.js';

let optionSelected = function(result) {
    console.log(GAMES[result]);
}

class Main extends React.Component {
    state = {
        ratings: []
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
                                method: "POST",
                                body: JSON.stringify(this.state)
                            }).then(response => {
                                console.log(response);
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