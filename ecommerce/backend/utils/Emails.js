const https = require('https')

exports.sendMail = async (receiverEmail, subject, body) => {
    const data = JSON.stringify({
        sender: {
            name: process.env.EMAIL_FROM_NAME || 'E-commerce App',
            email: process.env.EMAIL_FROM_ADDRESS || process.env.EMAIL
        },
        to: [{ email: receiverEmail }],
        subject: subject,
        htmlContent: body
    })

    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.brevo.com',
            path: '/v3/smtp/email',
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'api-key': process.env.BREVO_API_KEY,
                'content-type': 'application/json',
                'content-length': Buffer.byteLength(data)
            }
        }

        const req = https.request(options, (res) => {
            let body = ''
            res.on('data', chunk => body += chunk)
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(JSON.parse(body))
                } else {
                    reject(new Error(`Brevo API error ${res.statusCode}: ${body}`))
                }
            })
        })

        req.on('error', reject)
        req.write(data)
        req.end()
    })
}
