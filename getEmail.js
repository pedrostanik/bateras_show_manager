const imaps = require('imap-simple');
const { simpleParser } = require('mailparser');

// Configurações de conexão para o Outlook
const config = {
  imap: {
    user: 'pedro.ostanik@join4.com.br',
    password: 'Lpnaveiaaa2*',
    host: 'outlook.office365.com',
    port: 993,
    tls: true,
    authTimeout: 3000,
  },
};

// Função para buscar e-mails
async function fetchEmail() {
  try {
    const connection = await imaps.connect(config);

    // Abre a caixa de entrada
    await connection.openBox('INBOX');

    // Define critérios de busca (por exemplo, e-mails não lidos)
    const searchCriteria = ['UNSEEN'];

    // Define o que será retornado
    const fetchOptions = {
      bodies: ['HEADER', 'TEXT'],
      markSeen: true,
    };

    // Busca e-mails na caixa de entrada
    const messages = await connection.search(searchCriteria, fetchOptions);

    for (const item of messages) {
      const all = item.parts.find(part => part.which === 'TEXT');
      const id = item.attributes.uid;
      const idHeader = "Imap-Id: " + id + "\r\n";
      const mail = await simpleParser(idHeader + all.body);

      console.log('Assunto:', mail.subject);
      console.log('Texto:', mail.text);  // Texto do e-mail
    }

    await connection.end();
  } catch (error) {
    console.error('Erro ao buscar e-mail:', error);
  }
}

fetchEmail();
