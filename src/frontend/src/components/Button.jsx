const Button = (props) => {
  const buttonStyle = {
    color: "green",
    fontStyle: "italic",
    fontSize: "20px"
  }
  return (
    <button style={buttonStyle} onClick={props.clickFunction}>{props.text}</button>
  )
}

export default Button