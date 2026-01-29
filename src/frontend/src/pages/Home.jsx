import { useNavigate } from 'react-router-dom'
import Button from '../components/Button'
import { useState, useEffect } from 'react'
import leagueService from '../services/leagues'
import ViewLeague from '../components/ViewLeagues'


function Home() {
  const [leagues, setLeagues] = useState([])
  const [loading, setLoading] = useState(true)

  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  useEffect(() => {

    leagueService.getLeagues()
      .then(data => {
        setLeagues(data)
        setLoading(false)
      })
      .catch(err => {
        console.log(err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <p>Loading...</p>
  }

  return (
    <div>
      <h1>Home Page</h1>

      <p>You are logged in.</p>
      <ViewLeague leagues={leagues} />
      <Button text='Logout' clickFunction={logout} />
    </div>
  )
}

export default Home
