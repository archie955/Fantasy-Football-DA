const LoginHeader = ({ login }) => <h2>{login ? 'Login' : 'Create Account'}</h2>

const ButtonForm = ({ onClickFunction, text }) => <button type="button" onClick={onClickFunction}>{text}</button>

const LoginForm = (props) => {
  return (
    <form onSubmit={props.login ? props.loginFunction : props.createAccountFunction}>
      <div>
        <Header login={props.login}/><ButtonForm onClickFunction={props.changeLogin} text={'change'}/>
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
          onChange={e => props.setNewPasswordFunction(e.target.value)}/><ButtonForm onClickFunction={props.showPasswordFunction} text={props.visible ? 'Hide' : 'Show'}/>
      </div>
      <button type="submit">Submit</button>
    </form>
  )
}

export default LoginForm