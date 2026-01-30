import Button from './Button'

const ViewPlayers = (props) => {
    const players = props.players
    console.log(players)

    return (
        <ul>
            {players.map(player => {
                const playerString = `${player.position} ${player.name} - ${player.team} - ${player.fantasy_points_ppr}`
                return(
                    <li key={player.id}>
                        <Button text={playerString} clickFunction={props.navigationFunction(player)} />
                    </li>
                )
            }
            )}
        </ul>
    )
}

export default ViewPlayers