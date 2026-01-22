import { useState } from 'react'
import './App.css'
import loginServices from './services/login'

const Header = ({ login }) => <h2>{login ? 'Login' : 'Create Account'}</h2>

const LoginForm = (props) => {
  return (
    <form onSubmit={props.login ? props.loginFunction : props.createAccountFunction}>
      <div>
        <Header login={props.login}/><button type="button" onClick={props.changeLogin}>change</button>
      </div>
      <div>
        email: <input
          value={props.email}
          placeholder='Enter your email'
          onChange={e => props.setNewEmailFunction(e.target.value)}/>
      </div>
      <div>
        password: <input
          type={props.visible ? 'text':'password'}
          placeholder='Enter your password'
          value={props.password}
          onChange={e => props.setNewPasswordFunction(e.target.value)}/> <button type="button" onClick={props.showPasswordFunction}>{props.visible ? 'Hide' : 'Show'}</button>
      </div>
      <button type="submit">Submit</button>
    </form>
  )
}




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
