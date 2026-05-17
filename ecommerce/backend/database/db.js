require('dotenv').config()
const mongoose = require("mongoose")

exports.connectToDB = async () => {
    try {
        await mongoose.connect(process.env.MONGO_URI)
        console.log('connected to DB')
    } catch (error) {
        console.error('DB connection failed:', error.message)
        process.exit(1)
    }
}
