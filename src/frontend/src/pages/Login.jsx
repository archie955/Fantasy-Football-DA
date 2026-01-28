import { useState } from 'react'
import loginServices from '../services/login'
import LoginForm from '../components/LoginForm'
import Notification from '../components/Notification'
import { useNavigate } from 'react-router-dom'


function Login() {
  const [visible, setVisible] = useState(false);
  const [login, setLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [updateMessage, setUpdateMessage] = useState(null)

  const navigate = useNavigate()

  const showPassword = () => {
    setVisible(!visible)
  }

  const loginOrCreate = () => {
    setLogin(!login)
  }

  const loginFunction = (event) => {
    event.preventDefault()

    const person = {email: email, password: password}

    loginServices
      .loginAccount(person)
      .then(returnedPerson => {
        localStorage.setItem("token", returnedPerson.access_token)
        setEmail('')
        setPassword('')
        setUpdateMessage('Successfully logged in')

        setTimeout(() => {
          navigate('/home')
        }, 1000)
      })
  }

  const createAccountFunction = (event) => {
    event.preventDefault()

    const person = {email: email, password: password}

    loginServices
      .createAccount(person)
      .then(() => {
        setEmail('')
        setPassword('')
        setLogin(true)

        setUpdateMessage('Successfully created account')
        setTimeout(() => {
          setUpdateMessage(null)
        }, 4000)
      })
  }

  return (
    <div>
      <Notification message={updateMessage} />

      <LoginForm
        login={login} 
        loginFunction={loginFunction} 
        createAccountFunction={createAccountFunction}
        changeLogin={loginOrCreate} 
        visible={visible}
        showPasswordFunction={showPassword}
        email={email}
        setNewEmailFunction={setEmail}
        password={password}
        setNewPasswordFunction={setPassword}
      />
    </div>
  )
}

export default Login