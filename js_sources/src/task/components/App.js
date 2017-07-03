/*
 * File Name : app.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

import Mn from 'backbone.marionette';

const AppClass = Mn.Application.extend({
  region: '#js-main-area'
});
const App = new AppClass();
export default App;
