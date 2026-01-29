import Button from './Button'

const ViewLeague = (props) => {
    const leagues = props.leagues
    return (
        <ul>
            {leagues.map(league => 
                <li key={league.id}>
                    <Button text={league.name} clickFunction={props.navigationFunction(league)} />
                </li>
            )}
        </ul>
    )
}

export default ViewLeague