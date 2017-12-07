'use strict';

import React from 'react';
import { Typeahead } from 'react-typeahead';

const Main = () => <div>
        <div className="row">
            <h2>VGML</h2>
        </div>
        <div className="row typeahead">
            <Typeahead
                options={['Portal', 'League of Legends', 'Halo', 'COD']}
                maxVisible={2}
            />
        </div>
        
    </div>;

export default Main;