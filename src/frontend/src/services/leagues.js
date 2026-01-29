import api from './api'

const getLeagues = () => {
    const request = api.get('/fetchdata/')
    return request.then(response => response.data)
}

export default { getLeagues }