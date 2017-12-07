'use strict';

import React from 'react';
import { Typeahead } from 'react-typeahead';
import GAMES from '../games.js';

let optionSelected = function(result) {
    console.log(GAMES[result]);
}

const Main = () => <div>
        <div className="row">
            <h2>VGML</h2>
        </div>
        <div className="row typeahead">
            <Typeahead
                displayOption={option => option.game}
                filterOption="game"
                options={GAMES}
                maxVisible={10}
                onOptionSelected={optionSelected}
            />
        </div>
        
    </div>;

export default Main;