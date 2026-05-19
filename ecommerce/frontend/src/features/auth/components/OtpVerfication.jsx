import {FormHelperText, Paper, Stack, TextField, Typography } from '@mui/material'
import React, { useEffect, useState} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { clearOtpVerificationError, clearResendOtpError, clearResendOtpSuccessMessage, resendOtpAsync, resetOtpVerificationStatus, resetResendOtpStatus, selectLoggedInUser, selectOtpVerificationError, selectOtpVerificationStatus, selectResendOtpError, selectResendOtpStatus, selectResendOtpSuccessMessage, verifyOtpAsync } from '../AuthSlice'
import { LoadingButton } from '@mui/lab'
import { useNavigate } from 'react-router-dom'
import { useForm } from "react-hook-form"
import {toast} from 'react-toastify'


export const OtpVerfication = () => {
    
    const {register,handleSubmit,formState: { errors }} = useForm()
    const dispatch=useDispatch()
    const loggedInUser=useSelector(selectLoggedInUser)
    const navigate=useNavigate()
    const resendOtpStatus=useSelector(selectResendOtpStatus)
    const resendOtpError=useSelector(selectResendOtpError)
    const resendOtpSuccessMessage=useSelector(selectResendOtpSuccessMessage)
    const otpVerificationStatus=useSelector(selectOtpVerificationStatus)
    const otpVerificationError=useSelector(selectOtpVerificationError)

    // FIX: OTP form is always shown (OTP auto-sent on signup)
    // User can also resend if needed
    const [otpSent, setOtpSent] = useState(true)

    // handles the redirection
    useEffect(()=>{
        if(!loggedInUser){
            navigate('/login')
        }
        else if(loggedInUser && loggedInUser?.isVerified){
            navigate("/")
        }
    },[loggedInUser])

    const handleSendOtp=()=>{
        const data={user:loggedInUser?._id}
        dispatch(resendOtpAsync(data))
    }
    
    const handleVerifyOtp=(data)=>{
        const cred={...data,userId:loggedInUser?._id}
        dispatch(verifyOtpAsync(cred))
    }

    // handles resend otp error
    useEffect(()=>{
        if(resendOtpError){
            toast.error(resendOtpError.message)
        }
        return ()=>{
            dispatch(clearResendOtpError())
        }
    },[resendOtpError])

    // handles resend otp success message
    useEffect(()=>{
        if(resendOtpSuccessMessage){
            toast.success(resendOtpSuccessMessage.message)
            setOtpSent(true)
        }
        return ()=>{
            dispatch(clearResendOtpSuccessMessage())
        }
    },[resendOtpSuccessMessage])

    // handles error while verifying otp
    useEffect(()=>{
        if(otpVerificationError){
            toast.error(otpVerificationError.message)
        }
        return ()=>{
            dispatch(clearOtpVerificationError())
        }
    },[otpVerificationError])

    useEffect(()=>{
        if(otpVerificationStatus==='fullfilled'){
            toast.success("Email verified! We are happy to have you here")
            dispatch(resetResendOtpStatus())
        }
        return ()=>{
            dispatch(resetOtpVerificationStatus())
        }
    },[otpVerificationStatus])

  return (
    <Stack width={'100vw'} height={'100vh'} noValidate flexDirection={'column'} rowGap={3} justifyContent="center" alignItems="center" >

        <Stack component={Paper} elevation={1} position={'relative'} justifyContent={'center'} alignItems={'center'} p={'2rem'} rowGap={'2rem'} minWidth={'320px'}>
            
            <Typography mt={2} variant='h5' fontWeight={500}>Verify Your Email Address</Typography>

            <Stack width={'100%'} rowGap={'1rem'} component={'form'} noValidate onSubmit={handleSubmit(handleVerifyOtp)}>
                <Stack rowGap={'1rem'}> 
                    <Stack>
                        <Typography color={'GrayText'}>Enter the 4-digit OTP sent to</Typography>
                        <Typography fontWeight={'600'} color={'GrayText'}>{loggedInUser?.email}</Typography>
                    </Stack>
                    <Stack>
                        <TextField 
                            {...register("otp",{
                                required:"OTP is required",
                                minLength:{value:4,message:"Please enter a 4 digit OTP"},
                                maxLength:{value:4,message:"OTP must be exactly 4 digits"}
                            })} 
                            fullWidth 
                            type='number'
                            placeholder="Enter 4-digit OTP"
                        />
                        {errors?.otp && <FormHelperText sx={{color:"red"}}>{errors.otp.message}</FormHelperText>}
                    </Stack>
               </Stack>
                <LoadingButton loading={otpVerificationStatus==='pending'} type='submit' fullWidth variant='contained'>Verify OTP</LoadingButton>
                <LoadingButton 
                    onClick={handleSendOtp} 
                    loading={resendOtpStatus==='pending'} 
                    fullWidth 
                    variant='outlined'
                    size="small"
                >
                    Resend OTP
                </LoadingButton>
            </Stack>

        </Stack>
    </Stack>
  )
}
