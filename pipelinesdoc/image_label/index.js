const express = require('express');

const app = express();

app.use(express.static('dist'));

app.listen(3000, () => {
  // eslint-disable-next-line no-console
  console.log('App listening on port http://localhost:3000/ !');
});
