import axios from 'axios'

export const axiosi = axios.create({
    withCredentials: true,
    baseURL: process.env.REACT_APP_BASE_URL
})

// Global response interceptor — normalises every error into a consistent shape
// so all API files can safely do: throw error.response.data
axiosi.interceptors.response.use(
    (response) => response,
    (error) => {
        // Network error / server down / CORS — no response object at all
        if (!error.response) {
            return Promise.reject({
                message: error.message === 'Network Error'
                    ? 'Cannot reach server. Please check your connection or try again later.'
                    : error.message || 'An unexpected error occurred'
            })
        }
        // Server responded with an error status — pass through as-is
        return Promise.reject(error.response.data)
    }
)
