require('dotenv').config()
const nodemailer = require('nodemailer')

console.log('EMAIL:', process.env.EMAIL)
console.log('SMTP_HOST:', process.env.SMTP_HOST)

const t = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT),
    secure: false,
    auth: {
        user: process.env.EMAIL,
        pass: process.env.PASSWORD
    }
})

t.verify((err) => {
    if (err) {
        console.log('❌ FAILED:', err.message)
    } else {
        console.log('✅ Connected! Sending...')
        t.sendMail({
            from: process.env.EMAIL_FROM,
            to: process.env.EMAIL,
            subject: 'OTP Test',
            html: '<b>Your OTP is: 1234</b>'
        }, (e, info) => {
            if (e) console.log('❌ Send failed:', e.message)
            else console.log('✅ Sent:', info.messageId)
        })
    }
})
