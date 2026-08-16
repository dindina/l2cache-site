const token = process.argv[2];
const [header, payload, signature] = token.split('.');
console.log(JSON.stringify({
  header: JSON.parse(Buffer.from(header, 'base64').toString()),
  payload: JSON.parse(Buffer.from(payload, 'base64').toString()),
  signature
}, null, 2));
