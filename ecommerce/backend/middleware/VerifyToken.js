require('dotenv').config()
const jwt=require('jsonwebtoken')
const { sanitizeUser } = require('../utils/SanitizeUser')

exports.verifyToken=async(req,res,next)=>{
    try {
        const {token}=req.cookies

        if(!token){
            return res.status(401).json({message:"Token missing, please login again"})
        }

        // FIX: use same key as generateToken
        const decodedInfo=jwt.verify(token, process.env.JWT_SECRET || process.env.SECRET_KEY)

        if(decodedInfo && decodedInfo._id && decodedInfo.email){
            req.user=decodedInfo
            next()
        } else {
            return res.status(401).json({message:"Invalid token, please login again"})
        }
        
    } catch (error) {
        console.log(error);
        if (error instanceof jwt.TokenExpiredError) {
            return res.status(401).json({ message: "Token expired, please login again" });
        } else if (error instanceof jwt.JsonWebTokenError) {
            return res.status(401).json({ message: "Invalid token, please login again" });
        } else {
            return res.status(500).json({ message: "Internal Server Error" });
        }
    }
}
