const nodemailer = require("nodemailer");

// Transporter is created fresh per call so env vars are always read at runtime
// Supports Gmail (service:"gmail") and any SMTP relay like Brevo
const createTransporter = () => {
    // If SMTP_HOST is set, use raw SMTP config (Brevo, Mailgun, etc.)
    if (process.env.SMTP_HOST) {
        return nodemailer.createTransport({
            host: process.env.SMTP_HOST,
            port: parseInt(process.env.SMTP_PORT) || 587,
            secure: parseInt(process.env.SMTP_PORT) === 465, // true only for port 465
            auth: {
                user: process.env.EMAIL,
                pass: process.env.PASSWORD,
            },
        });
    }

    // Fallback: Gmail service shorthand
    return nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: process.env.EMAIL,
            pass: process.env.PASSWORD,
        },
    });
};

exports.sendMail = async (receiverEmail, subject, body) => {
    const transporter = createTransporter();
    await transporter.sendMail({
        from: process.env.EMAIL_FROM || process.env.EMAIL,
        to: receiverEmail,
        subject: subject,
        html: body,
    });
};
