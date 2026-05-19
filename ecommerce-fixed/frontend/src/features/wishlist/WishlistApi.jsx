import {axiosi} from '../../config/axios'

export const createWishlistItem=async(data)=>{
    try{const res=await axiosi.post("/wishlist",data);return res.data}
    catch(error){throw error}
}
export const fetchWishlistByUserId=async(id)=>{
    try{
        const res=await axiosi.get(`/wishlist/user/${id}`)
        const totalResults=res.headers['x-total-count']
        return {data:res.data, totalResults}
    }
    catch(error){throw error}
}
export const updateWishlistItemById=async(update)=>{
    try{const res=await axiosi.patch(`/wishlist/${update._id}`,update);return res.data}
    catch(error){throw error}
}
export const deleteWishlistItemById=async(id)=>{
    try{const res=await axiosi.delete(`/wishlist/${id}`);return res.data}
    catch(error){throw error}
}
