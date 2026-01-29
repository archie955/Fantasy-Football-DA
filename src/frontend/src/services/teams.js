import api from './api'

const getTeamsFromLeague = league => {
    console.log(league)
    const request = api.get(`/fetchdata/${league.id}`)
    return request.then(response => response.data)
}

export default { getTeamsFromLeague }