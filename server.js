const express = require('express');
const app = express();

app.get('*', (req, res) => {
    res.redirect(301, 'https://www.legacydunamis.com.br');
});

app.listen(process.env.PORT || 8080, () => {
    console.log('Servidor de redirecionamento rodando...');
});
