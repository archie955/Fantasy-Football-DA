import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import playerService from '../services/players'
import ViewPlayers from '../components/ViewPlayers'
import Button from '../components/Button'



function Players() {
    const [players, setPlayers] = useState([])
    const [loading, setLoading] = useState(true)

    const navigate = useNavigate()

    const returnToLeague = () => {
        localStorage.removeItem('team')
        navigate('/league')
    }

    const navigateParentFunction = (player) => {
        const playerToStore = JSON.stringify(player)
        const navigatePlayer = () => {
            console.log(playerToStore)
        }
        return navigatePlayer
    }

    useEffect(() => {
        const storedTeam = localStorage.getItem('team')

        if (!storedTeam) {
            navigate('/league')
            return
        }

        const team = JSON.parse(storedTeam)

        playerService.getPlayersFromTeam(team)
            .then(data => {
                setPlayers(data)
                setLoading(false)
            }).catch(err => {
                console.log(err)
                setLoading(false)
            })
    }, [])

    if (loading) {
        return <p>Loading...</p>
    }

    return (
        <div>
            <h1>This is the players page</h1>
            <ViewPlayers players={players} navigationFunction={navigateParentFunction} />
            <Button text='return to teams' clickFunction={returnToLeague} />
        </div>
    )
}

export default Players