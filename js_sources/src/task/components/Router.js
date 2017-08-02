/*
 * File Name : router.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

import Mn from 'backbone.marionette';

const Router = Mn.AppRouter.extend({
  appRoutes: {
      'login': 'login'
  }
});
export default Router;
