import { useState } from 'react'
import './App.css'
import loginServices from './services/login'
import LoginForm from './components/loginform'




function App() {
  const [visible, setVisible] = useState(false);
  const [login, setLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

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
        setEmail('')
        setPassword('')
        console.log('successfully logged in as', returnedPerson)
      })
  }

  const createAccountFunction = (event) => {
    event.preventDefault()
    const person = {email: email, password: password}
    loginServices
      .createAccount(person)
      .then(returnedPerson => {
        setEmail('')
        setPassword('')
        console.log('successfully created account', returnedPerson)
      })
  }

  return (
    <div>
      <LoginForm login={login} loginFunction={loginFunction} 
      createAccountFunction={createAccountFunction} changeLogin={loginOrCreate} 
      visible={visible} showPasswordFunction={showPassword}
      email={email} setNewEmailFunction={setEmail}
      password={password} setNewPasswordFunction={setPassword}/>
    </div>
  )
}

export default App
