const NewLeagueForm = (props) => {

    const handleSubmit = (e) => {
        e.preventDefault()

        const newLeague = {
            name: props.leagueName
        }

        props.submitFunction(newLeague)
    }
    return (
        <form onSubmit={handleSubmit}>
            <h2>Create a new league</h2>
            <div>
                League Name: <input
                    value={props.leagueName}
                    placeholder='Enter league name'
                    onChange={e => props.setNewLeagueName(e.target.value)}
                    />
            </div>
            <button type='submit'>Submit</button>
        </form>
    )
}

export default NewLeagueForm