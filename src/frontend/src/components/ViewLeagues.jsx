const ViewLeague = ({ leagues }) => {
    return (
        <ul>
            {leagues.map(league => 
                <li key={league.id}>
                    {league.name}
                </li>
            )}
        </ul>
    )
}

export default ViewLeague