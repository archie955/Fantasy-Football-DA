import axios from 'axios'
const baseUrl = 'http://127.0.0.1:8000/fetchdata/'

const getLeagues = () => {
    const token = localStorage.getItem("token")

    const config = {
        headers: {
        Authorization: `Bearer ${token}`
        }
    }

    const request = axios.get(baseUrl, config)
    return request.then(response => response.data)
}

export default { getLeagues }