import { useNavigate } from 'react-router-dom'
import ViewLeague from '../components/ViewLeagues'
import { useState, useEffect } from 'react'
import teamService from '../services/teams'
import Button from '../components/Button'


function Teams() {
    const [teams, setTeams] = useState([])
    const [loading, SetLoading] = useState(true)

    const navigate = useNavigate()

    const returnToHome = () => {
        localStorage.removeItem("league")
        navigate('/home')
    }

    const navigateParentFunction = (team) => {
        const toStoreTeam = JSON.stringify(team)
        const navigatePlayers = () => {
            console.log(toStoreTeam)
            localStorage.setItem('team', toStoreTeam)
            navigate('/team')
        }
        return navigatePlayers
    }

    useEffect(() => {
        const storedLeague = localStorage.getItem('league')

        if (!storedLeague) {
            navigate('/home')
            return
        }
        
        const league = JSON.parse(storedLeague)
        console.log('league: ', league)
        teamService.getTeamsFromLeague(league)
            .then(data => {
                setTeams(data)
                SetLoading(false)
            })
            .catch(err => {
                console.log(err)
                SetLoading(false)
            })
    }, [])

    if (loading) {
        return <p>Loading...</p>
    }

    return (
        <div>
            <h1>This is the teams page</h1>
            <ViewLeague leagues={teams} navigationFunction={navigateParentFunction} />
            <Button text='Return to home' clickFunction={returnToHome} />
        </div>
    )
    
}

export default Teams