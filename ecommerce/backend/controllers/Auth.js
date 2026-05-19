const User = require("../models/User");
const bcrypt=require('bcryptjs');
const { sendMail } = require("../utils/Emails");
const { generateOTP } = require("../utils/GenerateOtp");
const Otp = require("../models/OTP");
const { sanitizeUser } = require("../utils/SanitizeUser");
const { generateToken } = require("../utils/GenerateToken");
const PasswordResetToken = require("../models/PasswordResetToken");

// Helper to set auth cookie
const setAuthCookie = (res, token) => {
    const isProduction = process.env.PRODUCTION === 'true'
    res.cookie('token', token, {
        sameSite: isProduction ? "None" : 'Lax',
        maxAge: parseInt(process.env.COOKIE_EXPIRATION_DAYS || 30) * 24 * 60 * 60 * 1000,
        httpOnly: true,
        secure: isProduction
    })
}

exports.signup=async(req,res)=>{
    try {
        const existingUser=await User.findOne({email:req.body.email})
        
        if(existingUser){
            return res.status(400).json({"message":"User already exists"})
        }

        const hashedPassword=await bcrypt.hash(req.body.password,10)
        req.body.password=hashedPassword

        const createdUser=new User(req.body)
        await createdUser.save()

        const secureInfo=sanitizeUser(createdUser)
        const token=generateToken(secureInfo)
        setAuthCookie(res, token)

        // Auto-send OTP on signup (FIX: OTP was never sent automatically)
        const otp=generateOTP()
        const hashedOtp=await bcrypt.hash(otp,10)
        const newOtp=new Otp({
            user:createdUser._id,
            otp:hashedOtp,
            expiresAt:Date.now()+parseInt(process.env.OTP_EXPIRATION_TIME || 120000)
        })
        await newOtp.save()

        // Send OTP email — log the OTP to console as fallback so you can always test
        console.log(`\n📧 OTP for ${createdUser.email}: ${otp}\n`)
        try {
            await sendMail(
                createdUser.email,
                `OTP Verification for Your Account`,
                `Your One-Time Password (OTP) for account verification is: <b>${otp}</b>.<br/>Do not share this OTP with anyone for security reasons.`
            )
            console.log(`✅ OTP email sent to ${createdUser.email}`)
        } catch(emailErr) {
            console.log(`❌ OTP email FAILED:`, emailErr.message)
            // Don't fail signup if email fails — user can use console OTP or resend
        }

        res.status(201).json(sanitizeUser(createdUser))

    } catch (error) {
        console.log(error);
        res.status(500).json({message:"Error occured during signup, please try again later"})
    }
}

exports.login=async(req,res)=>{
    try {
        const existingUser=await User.findOne({email:req.body.email})

        if(existingUser && (await bcrypt.compare(req.body.password,existingUser.password))){

            // Block login if email not verified — resend OTP automatically
            if(!existingUser.isVerified){
                const secureInfo=sanitizeUser(existingUser)
                const token=generateToken(secureInfo)
                setAuthCookie(res, token)

                // Resend a fresh OTP
                await Otp.deleteMany({user:existingUser._id})
                const otp=generateOTP()
                const hashedOtp=await bcrypt.hash(otp,10)
                const newOtp=new Otp({
                    user:existingUser._id,
                    otp:hashedOtp,
                    expiresAt:Date.now()+parseInt(process.env.OTP_EXPIRATION_TIME || 120000)
                })
                await newOtp.save()
                console.log(`\n📧 OTP for ${existingUser.email}: ${otp}\n`)
                try {
                    await sendMail(
                        existingUser.email,
                        `OTP Verification for Your Account`,
                        `Your One-Time Password (OTP) for account verification is: <b>${otp}</b>.<br/>Do not share this OTP with anyone for security reasons.`
                    )
                } catch(e){ console.log('Email error:',e.message) }

                return res.status(200).json(sanitizeUser(existingUser))
            }

            const secureInfo=sanitizeUser(existingUser)
            const token=generateToken(secureInfo)
            setAuthCookie(res, token)
            return res.status(200).json(sanitizeUser(existingUser))
        }

        res.clearCookie('token');
        return res.status(404).json({message:"Invalid Credentials"})
    } catch (error) {
        console.log(error);
        res.status(500).json({message:'Some error occured while logging in, please try again later'})
    }
}

exports.verifyOtp=async(req,res)=>{
    try {
        const isValidUserId=await User.findById(req.body.userId)

        if(!isValidUserId){
            return res.status(404).json({message:'User not found'})
        }

        const isOtpExisting=await Otp.findOne({user:isValidUserId._id})

        if(!isOtpExisting){
            return res.status(404).json({message:'OTP not found. Please request a new OTP.'})
        }

        if(isOtpExisting.expiresAt < new Date()){
            await Otp.findByIdAndDelete(isOtpExisting._id)
            return res.status(400).json({message:"OTP has expired. Please request a new one."})
        }
        
        if(isOtpExisting && (await bcrypt.compare(req.body.otp,isOtpExisting.otp))){
            await Otp.findByIdAndDelete(isOtpExisting._id)
            const verifiedUser=await User.findByIdAndUpdate(isValidUserId._id,{isVerified:true},{new:true})
            return res.status(200).json(sanitizeUser(verifiedUser))
        }

        return res.status(400).json({message:'OTP is invalid or expired'})

    } catch (error) {
        console.log(error);
        res.status(500).json({message:"Some error occured"})
    }
}

exports.resendOtp=async(req,res)=>{
    try {
        const existingUser=await User.findById(req.body.user)

        if(!existingUser){
            return res.status(404).json({"message":"User not found"})
        }

        await Otp.deleteMany({user:existingUser._id})

        const otp=generateOTP()
        const hashedOtp=await bcrypt.hash(otp,10)

        const newOtp=new Otp({
            user:req.body.user,
            otp:hashedOtp,
            expiresAt:Date.now()+parseInt(process.env.OTP_EXPIRATION_TIME || 120000)
        })
        await newOtp.save()

        await sendMail(
            existingUser.email,
            `OTP Verification for Your Account`,
            `Your One-Time Password (OTP) for account verification is: <b>${otp}</b>.<br/>Do not share this OTP with anyone for security reasons.`
        )

        res.status(201).json({'message':"OTP sent successfully"})
    } catch (error) {
        res.status(500).json({'message':"Some error occured while sending OTP, please try again later"})
        console.log(error);
    }
}

exports.forgotPassword=async(req,res)=>{
    let newToken;
    try {
        const isExistingUser=await User.findOne({email:req.body.email})

        if(!isExistingUser){
            return res.status(404).json({message:"Provided email does not exist"})
        }

        await PasswordResetToken.deleteMany({user:isExistingUser._id})

        const passwordResetToken=generateToken(sanitizeUser(isExistingUser),true)
        const hashedToken=await bcrypt.hash(passwordResetToken,10)

        newToken=new PasswordResetToken({
            user:isExistingUser._id,
            token:hashedToken,
            expiresAt:Date.now() + parseInt(process.env.OTP_EXPIRATION_TIME || 120000)
        })
        await newToken.save()

        // FIX: use FRONTEND_URL env var for the reset link (backend ORIGIN is the frontend URL)
        const frontendUrl = process.env.FRONTEND_URL || process.env.ORIGIN || 'http://localhost:3000'

        await sendMail(
            isExistingUser.email,
            'Password Reset Link for Your Account',
            `<p>Dear ${isExistingUser.name},</p>
            <p>We received a request to reset the password for your account. If you initiated this request, please use the following link to reset your password:</p>
            <p><a href="${frontendUrl}/reset-password/${isExistingUser._id}/${passwordResetToken}" target="_blank">Reset Password</a></p>
            <p>This link is valid for a limited time. If you did not request a password reset, please ignore this email.</p>
            <p>Thank you,<br/>The Mern Shop Team</p>`
        )

        res.status(200).json({message:`Password reset link sent to ${isExistingUser.email}`})

    } catch (error) {
        console.log(error);
        res.status(500).json({message:'Error occured while sending password reset mail'})
    }
}

exports.resetPassword=async(req,res)=>{
    try {
        const isExistingUser=await User.findById(req.body.userId)

        if(!isExistingUser){
            return res.status(404).json({message:"User does not exist"})
        }

        const isResetTokenExisting=await PasswordResetToken.findOne({user:isExistingUser._id})

        if(!isResetTokenExisting){
            return res.status(404).json({message:"Reset link is not valid"})
        }

        if(isResetTokenExisting.expiresAt < new Date()){
            await PasswordResetToken.findByIdAndDelete(isResetTokenExisting._id)
            return res.status(404).json({message:"Reset link has expired"})
        }

        if(isResetTokenExisting && isResetTokenExisting.expiresAt>new Date() && (await bcrypt.compare(req.body.token,isResetTokenExisting.token))){
            await PasswordResetToken.findByIdAndDelete(isResetTokenExisting._id)
            await User.findByIdAndUpdate(isExistingUser._id,{password:await bcrypt.hash(req.body.password,10)})
            return res.status(200).json({message:"Password updated successfully"})
        }

        return res.status(404).json({message:"Reset link has expired"})

    } catch (error) {
        console.log(error);
        res.status(500).json({message:"Error occured while resetting the password, please try again later"})
    }
}

exports.logout=async(req,res)=>{
    try {
        const isProduction = process.env.PRODUCTION === 'true'
        res.cookie('token','',{
            maxAge:0,
            sameSite: isProduction ? "None" : 'Lax',
            httpOnly:true,
            secure: isProduction
        })
        res.status(200).json({message:'Logout successful'})
    } catch (error) {
        console.log(error);
        res.status(500).json({message:'Error during logout'})
    }
}

exports.checkAuth=async(req,res)=>{
    try {
        if(req.user){
            const user=await User.findById(req.user._id)
            if(!user) return res.sendStatus(401)
            return res.status(200).json(sanitizeUser(user))
        }
        res.sendStatus(401)
    } catch (error) {
        console.log(error);
        res.sendStatus(500)
    }
}
