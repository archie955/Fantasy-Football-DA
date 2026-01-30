import api from './api'

const getPlayersFromTeam = team => {
    const request = api.get(`/fetchdata/${team.league_id}/${team.id}`)
    return request.then(response => response.data)
}

const getOptimalLineup = team => {
    const request = api.get(`/trades/${team.league_id}/${team.id}/optimise`)
    return request.then(response => response.data)
}

export default { getPlayersFromTeam, getOptimalLineup }