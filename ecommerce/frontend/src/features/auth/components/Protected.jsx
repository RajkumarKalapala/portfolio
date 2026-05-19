import { useSelector } from "react-redux"
import { selectLoggedInUser } from "../AuthSlice"
import { Navigate } from "react-router"

export const Protected = ({children}) => {
    const loggedInUser = useSelector(selectLoggedInUser)

    // Not logged in at all → go to login
    if(!loggedInUser){
        return <Navigate to={'/login'} replace={true}/>
    }

    // Logged in but not verified → go to OTP page
    if(!loggedInUser.isVerified){
        return <Navigate to={'/verify-otp'} replace={true}/>
    }

    return children
}
