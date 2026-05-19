import {axiosi} from '../../config/axios'

export const addProduct=async(data)=>{
    try{const res=await axiosi.post('/products',data);return res.data}
    catch(error){throw error}
}

export const fetchProducts=async(filters)=>{
    let queryString=''
    if(filters.brand){
        filters.brand.forEach(b=>{ queryString+=`brand=${b}&` })
    }
    if(filters.category){
        filters.category.forEach(c=>{ queryString+=`category=${c}&` })
    }
    if(filters.pagination){
        queryString+=`page=${filters.pagination.page}&limit=${filters.pagination.limit}&`
    }
    if(filters.sort){
        queryString+=`sort=${filters.sort.sort}&order=${filters.sort.order}&`
    }
    if(filters.user){
        queryString+=`user=${filters.user}&`
    }
    try{
        const res=await axiosi.get(`/products?${queryString}`)
        // FIX: axios stores headers in lowercase; use res.headers directly (not .get())
        const totalResults=res.headers['x-total-count']
        return {data:res.data, totalResults}
    }
    catch(error){throw error}
}

export const fetchProductById=async(id)=>{
    try{const res=await axiosi.get(`/products/${id}`);return res.data}
    catch(error){throw error}
}
export const updateProductById=async(update)=>{
    try{const res=await axiosi.patch(`/products/${update._id}`,update);return res.data}
    catch(error){throw error}
}
export const undeleteProductById=async(id)=>{
    try{const res=await axiosi.patch(`/products/undelete/${id}`);return res.data}
    catch(error){throw error}
}
export const deleteProductById=async(id)=>{
    try{const res=await axiosi.delete(`/products/${id}`);return res.data}
    catch(error){throw error}
}
