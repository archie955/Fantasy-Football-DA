import api from './api'

const getLeagues = () => {
    const request = api.get('/fetchdata/')
    return request.then(response => response.data)
}

const createNewLeague = async (newLeague) => {
    const request = await api.post('/leagues/', newLeague)
    return request.data
}

export default { getLeagues, createNewLeague }